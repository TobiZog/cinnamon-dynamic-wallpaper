/**
 * @name	Cinnamon-Dynamic-Wallpaper
 * @alias 	TobiZog
 * @since	2023-08-25
 * 
 * @description Handles communications with the user (notifications, logs)
 */

/******************** Imports ********************/

const St = imports.gi.St;
const Main = imports.ui.main;
const Util = imports.misc.util;
const MessageTray = imports.ui.messageTray;
const UUID = "cinnamon-dynamic-wallpaper@TobiZog";
const DIRECTORY = imports.ui.extensionSystem.extensionMeta[UUID];



/******************** Functions ********************/

/**
 * Displaying a desktop notification
 * 
 * @param {string} title 				The Title in the notification
 * @param {string} text 				The text in the notification
 * @param {boolean} showOpenSettings 	Display the "Open settings" button in the notification, 
 * 										defaults to false
 */
function showNotification(title, text, showOpenSettings = false) {
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
			Util.spawnCommandLine("/usr/bin/env python3 " + 
				DIRECTORY.path + "/preferences/preferences.py"));
	}

	// Put all together
	Main.messageTray.add(source);

	// Display it
	source.notify(notification);
}