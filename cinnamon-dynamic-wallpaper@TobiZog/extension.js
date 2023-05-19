/**
 * @name	Cinnamon-Dynamic-Wallpaper
 * @alias 	TobiZog
 * @since	2023
 */

/******************** Imports ********************/

const MessageTray = imports.ui.messageTray;
const St = imports.gi.St;
const Main = imports.ui.main;
const Util = imports.misc.util;
const Settings = imports.ui.settings;
const { find_program_in_path } = imports.gi.GLib;
const Gio = imports.gi.Gio;


/******************** Constants ********************/

const UUID = "cinnamon-dynamic-wallpaper@TobiZog";
const APPNAME = "Cinnamon Dynamic Wallpaper"
const DIRECTORY = imports.ui.extensionSystem.extensionMeta[UUID];


/******************** Global Variables ********************/

// The extension object
let extension;


/******************** Objects ********************/

function CinnamonDynamicWallpaperExtension(uuid) {
	this._init(uuid);
}


CinnamonDynamicWallpaperExtension.prototype = {
	/**
	 * Initialization
	 * 
	 * @param {string} uuid 	Universally Unique Identifier
	 */
	_init: function(uuid) {
		this.settings = new Settings.ExtensionSettings(this, uuid);

		this.bindSettings("sw_auto_location", "autolocation")
		this.bindSettings("sc_location_refresh_time", "locationRefreshTime")
		this.bindSettings("etr_latitude", "latitude")
		this.bindSettings("etr_longitude", "longitude")
		this.bindSettings("etr_img_morning_twilight", "img_morning_twilight")
		this.bindSettings("etr_img_sunrise", "img_sunrise")
		this.bindSettings("etr_img_morning", "img_morning")
		this.bindSettings("etr_img_noon", "img_noon")
		this.bindSettings("etr_img_afternoon", "img_afternoon")
		this.bindSettings("etr_img_evening", "img_evening")
		this.bindSettings("etr_img_sunset", "img_sunset")
		this.bindSettings("etr_img_night_twilight", "img_night_twilight")
		this.bindSettings("etr_img_night", "img_night")
	},


	bindSettings: function (ui_name, js_name, func = this.on_settings_changed) {
		this.settings.bindProperty(
			Settings.BindingDirection.IN,
			ui_name,
			js_name,
			func
		)
	},


	/**
	 * Displaying a desktop notification
	 * 
	 * @param {string} title 				The Title in the notification
	 * @param {string} text 				The text in the notification
	 * @param {boolean} showOpenSettings 	Display the "Open settings" button in the notification, defaults to false
	 */
	showNotification: function (title, text, showOpenSettings = false) {
		let source = new MessageTray.Source(this.uuid);

		// Parameter
		let params = {
			icon: new St.Icon({
				icon_name: "icon",
				icon_type: St.IconType.FULLCOLOR,
				icon_size: source.ICON_SIZE
			})
		};

		// The notification itself
		let notification = new MessageTray.Notification(source, title, text, params);

		// Display the "Open settings" button, if showOpenSettings
		if (showOpenSettings) {
			notification.addButton("open-settings", _("Open settings"));

			notification.connect("action-invoked", () =>
				Util.spawnCommandLine("xlet-settings extension " + UUID));
		}

		// Put all together
		Main.messageTray.add(source);

		// Display it
		source.notify(notification);
	},


	/**
	 * Changes the desktop background image
	 * 
	 * @param {jpg} imageURI 	The new desktop image
	 */
	changeWallpaper: function(imageURI) {
		let gSetting = new Gio.Settings({schema: 'org.cinnamon.desktop.background'});
		gSetting.set_string('picture-uri', imageURI);
		Gio.Settings.sync();
		gSetting.apply();
	},


	/******************** UI Callbacks ********************/


	on_settings_changed: function () {
		// todo
	},


	/**
	 * Callback for settings-schema
	 * Opens the external heic-importer window
	 */
	openImageConfigurator: function() {
		Util.spawnCommandLine("/usr/bin/env python3 " + DIRECTORY.path + "/image-configurator/image-configurator.py");
	},


	/**
	 * Callback for settings-schema
	 * Opens the browser and navigate to the URL of the respository
	 */
	openRepoWebsite: function() {
		Util.spawnCommandLine("xdg-open https://github.com/TobiZog/cinnamon-dynamic-wallpaper");
	}
}



/******************** Lifecycle ********************/

/**
 * Lifecycle function on initialization
 * 
 * @param {*} extensionMeta 	Metadata of the extension
 */
function init(extensionMeta) {
	extension = new CinnamonDynamicWallpaperExtension(extensionMeta.uuid);
}


/**
 * Lifecycle function on enable
 * 
 * @returns The extension object
 */
function enable() {
	// Check for necessary software
	if (!find_program_in_path('heif-convert')) {
		Util.spawnCommandLine("apturl apt://libheif-examples");
	}

	// Display the welcome notification on activation
	extension.showNotification(
		APPNAME,
		"Welcome to " + APPNAME + "! Open the settings and configure the extensions.",
		true
	);

	return extension;
}


/**
 * Lifecycle function on disable
 */
function disable() {
	// todo
}