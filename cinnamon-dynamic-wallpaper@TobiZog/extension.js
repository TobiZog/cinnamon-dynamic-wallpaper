/**
 * @name	Cinnamon-Dynamic-Wallpaper
 * @alias 	TobiZog
 * @since	2023
 */


/********** Constants **********/

const UUID = "cinnamon-dynamic-wallpaper@TobiZog";
const APPNAME = "Cinnamon Dynamic Wallpaper"
const DIRECTORY = imports.ui.extensionSystem.extensionMeta[UUID];


/********** Imports **********/

const MessageTray = imports.ui.messageTray;
const St = imports.gi.St;
const Main = imports.ui.main;
const Util = imports.misc.util;
const Settings = imports.ui.settings;
const { find_program_in_path } = imports.gi.GLib;


/********** Global Variables **********/

// The extension object
let extension;


/********** Objects **********/

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
		this.settings = new Settings.AppletSettings(this, uuid);
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
	 * Callback for settings-schema
	 * Opens the external heic-importer window
	 */
	openImageConfigurator: function() {
		global.log(DIRECTORY.path + "/image-configurator/image-configurator.py")
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



/********** Lifecycle **********/

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