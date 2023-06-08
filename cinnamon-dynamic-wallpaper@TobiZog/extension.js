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
const Mainloop = imports.mainloop;
const Lang = imports.lang;
const { find_program_in_path } = imports.gi.GLib;
const Gio = imports.gi.Gio;

let suntimes = require('./scripts/suntimes')
let location = require('./scripts/location')


/******************** Constants ********************/

const UUID = "cinnamon-dynamic-wallpaper@TobiZog";
const APPNAME = "Cinnamon Dynamic Wallpaper"
const DIRECTORY = imports.ui.extensionSystem.extensionMeta[UUID];
const PATH = DIRECTORY.path;


/******************** Global Variables ********************/

// The extension object
let extension;

// Time and date of the last location update
let lastLocationUpdate = new Date()

// The last calculated suntime of the day
let lastDayTime = suntimes.DAYPERIOD.NONE

let looping = true


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

		this.bindSettings("sw_auto_location", "autolocation", this.updateLocation)
		this.bindSettings("sc_location_refresh_time", "locationRefreshTime")
		this.bindSettings("etr_latitude", "latitude", this.updateLocation)
		this.bindSettings("etr_longitude", "longitude", this.updateLocation)
		this.bindSettings("etr_img_morning_twilight", "img_morning_twilight", this.setImageToTime)
		this.bindSettings("etr_img_sunrise", "img_sunrise", this.setImageToTime)
		this.bindSettings("etr_img_morning", "img_morning", this.setImageToTime)
		this.bindSettings("etr_img_noon", "img_noon", this.setImageToTime)
		this.bindSettings("etr_img_afternoon", "img_afternoon", this.setImageToTime)
		this.bindSettings("etr_img_evening", "img_evening", this.setImageToTime)
		this.bindSettings("etr_img_sunset", "img_sunset", this.setImageToTime)
		this.bindSettings("etr_img_night_twilight", "img_night_twilight", this.setImageToTime)
		this.bindSettings("etr_img_night", "img_night", this.setImageToTime)

		this.setImageToTime()

		this._loop()
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



	setImageToTime: function() {
		let times = suntimes.calcTimePeriod(this.latitude, this.longitude)
		let now = new Date()

		let timesArray = [
			times["morning_twilight"], times["sunrise"], times["morning"],
			times["noon"], times["afternoon"], times["evening"], 
			times["sunset"], times["night_twilight"], times["night"]
		]

		let imageSet = [
			this.img_morning_twilight, this.img_sunrise, this.img_morning,
			this.img_noon, this.img_afternoon, this.img_evening,
			this.img_sunset, this.img_night_twilight, this.img_night
		]

		for(let i = 0; i < timesArray.length; i++) {
			if(timesArray[i][0] <= now && now <= timesArray[i][1] && i != lastDayTime) {
				this.changeWallpaper("file://" + PATH + "/res/custom_images/" + imageSet[i])

				lastDayTime = i
				break
			}
		}		
	},


	updateLocation: function () {
		if (this.autolocation) {
			let loc = location.estimateLocation()
			this.latitude = loc["latitude"]
			this.longitude = loc["longitude"]
		} else {
			this.latitude = this.latitude
			this.longitude = this.longitude
		}

		// Refresh the image information, if it's necessary
		this.setImageToTime()

		// Update the update information
		lastLocationUpdate = new Date()
	},


	/******************** UI Callbacks ********************/

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
	},


	/**
	 * Main loop
	 */
	_loop: function() {
		if(looping) {
			this.setImageToTime()

			if (lastLocationUpdate < new Date().getTime() - this.locationRefreshTime * 1000) {
				this.updateLocation()
				lastLocationUpdate = new Date()
			}
			
			// Refresh every 60 seconds
			Mainloop.timeout_add_seconds(60, Lang.bind(this, this._loop));
		}
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
	// extension.showNotification(
	// 	APPNAME,
	// 	"Welcome to " + APPNAME + "! Open the settings and configure the extensions.",
	// 	true
	// );

	return extension;
}


/**
 * Lifecycle function on disable
 */
function disable() {
	looping = false
}