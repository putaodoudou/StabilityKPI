#!/usr/bin/env python
# -*- coding: utf-8 -*-

from UiAutoTestLib import UiTestLib
import time
import re
import random

class UiKpiTest(UiTestLib):
    """
    Test Lib for Ui Automation test
    """
    def __init__(self, Serial = None):
        UiTestLib.__init__(self, Serial)
    #################################################
    #
    #       Telephony and phonebook
    #################################################
    def dial_number(self, number):
        try:
            self.open_application("com.android.dialer/.DialtactsActivity --activity-clear-top")
            self.wait_for_ui_exists(1500, resourceId="com.android.dialer:id/floating_action_button")
            self.click_ui(resourceId="com.android.dialer:id/floating_action_button")
            self.type_text(number, resourceId="com.android.dialer:id/digits")
            time.sleep(1)
            self.click_ui(resourceId="com.android.dialer:id/dialpad_floating_action_button")
        except Exception, e:
            print Exception, ":", e
            print "Exception happens"
            return False
        
    def add_new_contact(self, name, number):
        """Add contact with name and number"""
        add_btn = 'com.android.contacts:id/floating_action_button'
        save_btn = 'com.android.contacts:id/save_menu_item'
        if self.wait_for_ui_exists(1000, resourceId=add_btn):
            self.click_ui(resourceId=add_btn)
        else:
            return False
        
        self.wait_for_ui_exists(1000, text='Add new contact')
        self.type_text(name, text='Name', className='android.widget.EditText')
        self.type_text(number, text='Phone', className='android.widget.EditText')
        self.click_ui(resourceId=save_btn)
    
    def delete_contact(self, name):
        """delete contacts"""
        large_icon = 'com.android.contacts:id/photo_touch_intercept_overlay'
        if self.scroll_to_find(text=name):
            self.click_ui(text=name)
            self.wait_for_ui_exists(1000, resourceId=large_icon)
            self.press_key('menu')
            self.click_ui(text='Delete')
            self.click_ui(text="OK")
        else:
            return False

    def wait_and_connection(self, timeout=8):
        """Wait 5 seconds to end call when connected."""
        start = time.time()
        while (time.time() - start) < int(timeout):
            status = self.get_call_status()
            #print status
            if status == '2':
                return True                
            else:
                time.sleep(1)
        return False
    
    def wait_end_call(self, timeout = 4):
        try:
            if self.wait_and_connection(8):
                self.wait_for_ui_gone(15000, textContains="Calling via")
                self.logmsg("Calling via end")
                self.wait_for_ui_exists(8000, resourceId='com.android.dialer:id/elapsedTime')
                time.sleep(int(timeout))
                status = self.get_call_status()
                if status == '2':
                    self.logmsg("End call because it in calling")
                    self.press_key('6')   #end call key
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            print "Exception happens"
            return False
    ##################################
    #
    #       Messaging
    #
    ##################################
    def open_message_app(self):
        self.open_application('com.android.mms/.ui.ConversationList')
        return self.wait_for_ui_exists(3000, packageName='com.android.mms')
    
    def create_new_message(self):
        #com.android.mms:id/floating_action_button
        #com.android.mms:id/recipients_editor
        #com.android.mms:id/embedded_text_editor  Type message
        #send com.android.mms:id/send_button_sms
        #com.android.mms:id/send_button_mms  MMS
        pass
    
    def open_message(self, content):
        """open message by content"""
        try:
            if not self.wait_for_ui_exists(500, textContains=content):
                if self.scroll_to_find(textContains=content):
                    self.click_ui(textContains=content)
                    return True
            else:
                self.click_ui(textContains=content)
                return True
        except Exception, e:
            print Exception, ":", e
            self.logmsg("open message failed.")
            return False
            
    def forward_message(self, phoneNum, content, mms):
        """preconditon: open message
        phoneNum: to send to
        content: message to find and forward.
        """
        print 'mms:',mms
        try:
            if not self.wait_for_ui_exists(500, textContains=content):
                self.scroll_to_find(textContains=content)
            self.long_click_ui(textContains=content)
            #wait for com.android.mms:id/forward
            forward_btn = 'com.android.mms:id/forward'
            if self.wait_for_ui_exists(2000, resourceId=forward_btn):
                self.click_ui(resourceId=forward_btn)
                recipt_editor = 'com.android.mms:id/recipients_editor'
                self.wait_for_ui_exists(1000, resourceId=recipt_editor)
                self.type_text(phoneNum, resourceId=recipt_editor)
                if mms == 'True':
                    self.click_ui(resourceId='com.android.mms:id/send_button_mms')
                    time.sleep(5)
                else:
                    self.click_ui(resourceId='com.android.mms:id/send_button_sms')
                time.sleep(1)
                self.press_key('back')  #input method
                self.press_key('back')  #msg list
                self.open_message_app()
                if mms == 'True':
                    return self.wait_for_ui_exists(2000, textContains='Fwd:')
                else:
                    return self.wait_for_ui_exists(2000, textContains='Me:')
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Forward message exception happens.")
            return False
    
    def delete_msg_by_phoneNum(self, contact):
        """precondition: conversation mode
        long press phone number/contact name to delete conversation
        """
        try:
            self.open_message_app()
            self.long_click_ui(textContains=contact)
            delete_btn = 'com.android.mms:id/delete'
            if self.wait_for_ui_exists(2000, resourceId=delete_btn):
                self.click_id(delete_btn)
                self.click_ui(resourceId="android:id/button1")  #confirm delete
                return True
            return not self.wait_for_ui_exists(300, text=contact)
        except Exception, e:
            print Exception, ":", e
            return False
      
    def play_slideshow_mms(self):
        """precondition: the mms is opened"""
        id_slideshow = 'com.android.mms:id/play_slideshow_button'
        try:
            if self.wait_for_ui_exists(2000, resourceId=id_slideshow):
                self.click_id(id_slideshow)
                return self.wait_for_ui_exists(1000, text="Message details")
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Play slide show exception happens.")
            return False
    
    #################################################
    #
    #  Browser test cases
    #
    #################################################
    def open_browser_app(self):
        """Open browser application"""
        self.open_application('com.android.swe.browser/com.android.browser.BrowserLauncher')
        return self.wait_for_ui_exists(3000, packageName='com.android.swe.browser')
    
    def close_browser_app(self):
        moreBtn = 'com.android.browser:id/more_browser_settings'
        self.press_key('menu')
        self.scroll_to_find(text='Exit')
        self.click_text('Exit')
        self.click_id("android:id/button1") #Quit
        return not self.wait_for_ui_exists(300, packageName='com.android.swe.browser')
    
    def clear_browser_privacy(self):
        """preconditon: in browser main window
        postcondition: in browser main window"""
        moreBtn = 'com.android.browser:id/more_browser_settings'
        try:
            if self.wait_for_ui_exists(500, resourceId=moreBtn):
                self.click_id(moreBtn)
                self.click_text('Settings')
                self.click_text("Privacy & security")
                self.click_text('Clear stored data')
                self.click_text('Clear selected items')
                self.click_id("android:id/button1") #OK
                #go to browser main window
                self.press_key('back')
                self.press_key('back')
                self.press_key('back')
                return self.wait_for_ui_exists(800, resourceId=moreBtn)
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Clear browser privacy exception happens")
            return False
    
    def open_page(self, url='http://news.baidu.com'):
        """precodtion: in browser main window"""
        try:
            self.type_text(url, resourceId='com.android.browser:id/url')
            self.press_key('enter')
            time.sleep(2)
            return self.wait_for_ui_exists(6000, textContains='m.baidu.com/news?from')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open Page Failed.')
            return False
    
    def open_download_file(self, fileName):
        """Download file"""
        try:
            self.open_application('com.android.providers.downloads.ui/.DownloadList')
            downList = self.wait_for_ui_exists(1000, resourceId='com.android.documentsui:id/toolbar')
            if downList:
                self.wait_for_ui_exists(800, textContains=fileName)
                self.click_ui(textContains=fileName)
                return True
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open failed.')
            return False
            
    def verify_open(self, appName, **selectors):
        """Verify intent open files, try to use appName to open and verify **selectors"""
        try:
            if self.wait_for_ui_exists(800, textContains='Open with'):
                if self.wait_for_ui_exists(300, text=appName):
                    self.click_text(appName)
                time.sleep(2)
                if self.wait_for_ui_exists(500, resourceId='android:id/button_once'):
                    self.click_id('android:id/button_once')
            return self.wait_for_ui_exists(8000, **selectors)
        except Exception, e:
            print Exception, ":", e
            self.logmsg("Verified Failed")
            return False
    
    def delete_file_in_downloads(self, fileName):
        try:
            self.open_application('com.android.providers.downloads.ui/.DownloadList')
            downList = self.wait_for_ui_exists(2000, resourceId='com.android.documentsui:id/toolbar')
            print downList
            if downList:
                self.wait_for_ui_exists(800, textContains=fileName)
                self.long_click_ui(textContains=fileName)
                self.click_ui(description='More options')  #delete button
                return self.wait_for_ui_gone(2000, textContains=fileName)
            else:
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('delete failed.')
            return False
    
    #############################################
    #
    #       Home Icon Open
    #
    #############################################
    def open_app_from_Home(self, appName, packageName):
        """open Application from Home Launcher3"""
        try:
            self.press_key('home')
            # try 5 times to find app name on home
            if self.wait_for_ui_exists(500, text=appName):
                self.click_text(appName)
                return self.wait_for_ui_exists(5000, packageName=packageName)
            self.fling_toBeginning(oritation='horiz')
            for i in range(5):
                if self.wait_for_ui_exists(800, text=appName):
                    self.click_text(appName)
                    break
                else:
                    self.fling_forward(oritation='horiz')
                    time.sleep(0.3)
            result=self.wait_for_ui_exists(5000, packageName=packageName)
            if not result:
                self.logmsg('Open App %s Failed' % appName)
            return result
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open application %s exception' % appName)
            return False
    
    ################## Multimedia ###################
    def open_recorder_app(self):
        """open recorder"""
        try:
            self.open_application('com.cloudminds.soundrecorder/.SoundRecorderActivity')
            ckId='com.cloudminds.soundrecorder:id/bg_recorder_home_mike_nor'
            return self.wait_for_ui_exists(2000, resourceId=ckId)
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Open Recorder Failed in 2sec')
            return False
    def delete_record_files(self):
        try:
            lstHome='com.cloudminds.soundrecorder:id/btn_recorder_home_list'
            ckb = 'com.cloudminds.soundrecorder:id/select_checkbox'
            deleteBtn = 'com.cloudminds.soundrecorder:id/delectOrShare'
            
            uiStatus = self.check_record_ui_status()
            if uiStatus == 0:
                self.click_id(lstHome)
            elif uiStatus == 1:
                pass
            elif uiStatus == 3:
                self.press_key('back')
            else:
                return False
            if self.wait_for_ui_exists(1000, text='there is no file'):
                self.logmsg('There is no files to delete')
                return True
            self.click_ui(description='More options')  #more button
            self.click_text('delete')
            self.click_id(ckb)
            self.click_id(deleteBtn)
            self.click_id('android:id/button1')
            time.sleep(0.2)
            return not self.wait_for_ui_exists(1000, textMatches="Voice\d+\..*")
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Delete failed.')
            return False
    
    def check_record_ui_status(self):
        """return status 0, 1, 2, 3
        0  --- main window
        1   -- saved recordings window
        2   -- Select voice recordings
        """
        if self.wait_for_ui_exists(300, text='Sound Recorder'):
            return 0
        elif self.wait_for_ui_exists(300, text='Saved Recordings'):
            return 1
        elif self.wait_for_ui_exists(300, text='Select voice recordings'):
            return 3
        elif self.wait_for_ui_exists(300, resourceIdMatches='.*/search_text'):
            return 2
        
        else:
            return 255
    
    def record_voice(self, duration):
         #com.cloudminds.soundrecorder:id/text_time
         #com.cloudminds.soundrecorder:id/btn_recorder_home_recording
         #com.cloudminds.soundrecorder:id/btn_recorder_home_list
         #com.cloudminds.soundrecorder:id/ico_recorder_home_circle_3
         #org.codeaurora.snapcam:id/preview_thumb
         """stauts"""
         try:
             status = self.check_record_ui_status()
             if status == 0:
                self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             elif status == 1:
                 self.click_ui(resourceIdMatches='.*btn_recorder_list_recording')
             elif status == 3:
                 self.press_key('back')
                 self.press_key('back')
                 self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             else:
                 return False
             
             self.wait_for_ui_exists(3000, resourceIdMatches='.*ico_recorder_home_circle_3')
             time.sleep(int(duration))
             self.click_ui(resourceIdMatches='.*btn_recorder_home_recording')
             time.sleep(1)
             return self.wait_for_ui_exists(1000, textMatches="Voice\d+\..*")
             
         except Exception, e:
             print Exception, ":", e
             self.logmsg('Record voice failed.')
             return False
             
    def play_recorded_voice(self):
        #com.cloudminds.soundrecorder:id/seekBar
        try:
            uiStatus = self.check_record_ui_status()
            if uiStatus == 0:
                self.click_ui(resourceIdMatches='.*btn_recorder_home_list')
            elif uiStatus == 1:
                pass
            elif uiStatus == 3:
                self.press_key('back')
            else:
                return False
            if self.wait_for_ui_exists(1000, text='there is no file'):
                self.logmsg('There is no files to delete')
                return False
            self.click_ui(resourceIdMatches='.*recording_name')
            time.sleep(4)
            return self.wait_for_ui_exists(3000, resourceIdMatches='.*seekBar')
        except:
            self.logmsg('Play sound error')
            return False
            
    def open_music_app(self):
        """"""
        try:
            self.open_application('com.cloudminds.music2/.ui.activities.HomeActivity')
            return self.wait_for_ui_exists(3000, packageName='com.cloudminds.music2')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Exception when open music app')
            return False
            
    def play_music_shuffle_all(self):
        #audio_player_current_time
        #action_button_play
        #music name: bottom_action_bar_line_one
        #playing UI: action_button_previous, action_button_next
        try:
            self.click_ui(description='More options')
            self.click_text('Shuffle all')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Play music shuffle all Exception happens')
            return False
            
    def open_ongoing_music(self):
        try:
            self.click_ui(resourceIdMatches='.*/bottom_action_bar_line_one')
            return self.wait_for_ui_exists(2000, resourceIdMatches='.*/action_button_previous')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('open ongoing music failed, exception happens.')
            return False
    
    def play_next_music(self, duration):
        try:
            if not self.wait_for_ui_exists(800, resourceIdMatches='.*/action_button_previous'):
                return False
            self.click_ui(resourceIdMatches='.*/action_button_next')
            time.sleep(int(duration))
            return self.wait_for_ui_exists(300, resourceIdMatches='.*/action_button_previous')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Playing next music failed, exception happens.')
            return False
    def pause_music_playing(self):
        try:
            self.open_notification()
            if self.wait_for_ui_exists(3000, description='Pause', resourceIdMatches='.*action0'):
                self.click_ui(description='Pause', resourceIdMatches='.*action0')
            return self.wait_for_ui_exists(3000, description='Play', resourceIdMatches='.*action0')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Stop music playing failed or no playing music')
            return False
    
    ##### Camera  #####
    def open_camera_app(self):
        """"""
        #org.codeaurora.snapcam:id/filmstrip_bottom_controls   --video mode
        #org.codeaurora.snapcam:id/shutter_button
        #org.codeaurora.snapcam:id/camera_switcher  
        #org.codeaurora.snapcam:id/mdp_preview_content ---still mode
        #org.codeaurora.snapcam:id/preview_thumb
        try:
            self.open_application('org.codeaurora.snapcam/com.android.camera.CameraLauncher')
            return self.wait_for_ui_exists(8000, resourceIdMatches='.*shutter_button')
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Exception happens when openning camera app')
            return False
    
    def open_camera_mode(self, mode):
        """
        still --- still mode
        video --- video mode
        """
        #Switch to photo
        #Switch to video
        #Switch to panorama
        try:
            #film = self.wait_for_ui_exists(1000, resourceIdMatches='.*filmstrip_bottom_controls')
            mdp = self.wait_for_ui_exists(1000, resourceIdMatches='.*mdp_preview_content')
            if mode == 'still':
                self.click_ui(resourceIdMatches='.*camera_switcher')
                time.sleep(1)
                self.click_description('Switch to photo')
                time.sleep(1)
                return self.wait_for_ui_exists(1000, resourceIdMatches='.*mdp_preview_content')
            elif mode == 'video':
                self.click_ui(resourceIdMatches='.*camera_switcher')
                time.sleep(1)
                self.click_description('Switch to video')
                time.sleep(1)
                return self.wait_for_ui_exists(2000, resourceIdMatches='.*filmstrip_bottom_controls')
            else:
                self.logmsg('Please give correct video, still parameter')
                return False
        except Exception, e:
            print Exception, ":", e
            self.logmsg('Switch camera Exception')
            return False
    
    def capture_picture_video(self, mode, duration=60):
        """"""
        try:
            
            if mode=='still':
                self.open_camera_mode('still')
                self.click_ui(resourceIdMatches='.*shutter_button')
                time.sleep(3)
                return True
            elif mode=='video':
                self.open_camera_mode('video')
                self.click_ui(resourceIdMatches='.*shutter_button')
                time.sleep(int(duration))
                self.click_ui(resourceIdMatches='.*shutter_button')
            else:
                self.logmsg('cannot switch to still mode')
                return False
        except Exception, e:
            print Exception, ":", e
            return False
    def open_file_from_camera(self, delete='False'):
        #com.android.gallery3d:id/photopage_bottom_controls
        #com.android.gallery3d:id/photopage_bottom_controls
        #com.android.gallery3d:id/gl_root_view
        try:
            self.click_ui(resourceIdMatches='.*preview_thumb')
            self.press_key('menu')
            #double press menu if menu is not there
            if not self.wait_for_ui_exists(400, text='Delete'):
                self.press_key('menu')
            if self.wait_for_ui_exists(400, text='Mute'):
                self.logmsg('it is a movie')
                self.press_key('back')
                self.click_ui(resourceIdMatches='.*gl_root_view')
                self.verify_open('VideoPlayer', resourceIdMatches='.*videoProgress')
                #MTBF playing for 10s
                time.sleep(10)
                if not self.wait_for_ui_exists(1000, resourceIdMatches='.*photopage_bottom_controls'):
                    self.press_key('back')
                self.delete_files_gallery_view(delete)
                return True
                
            elif self.wait_for_ui_exists(400, text='Slideshow'):
                self.logmsg('it is a photo')
                self.press_key('back')
                self.delete_files_gallery_view(delete)
                return True
                
        except Exception, e:
            print Exception, ":", e
            self.logmsg('no picture or exception happens')
            return False
            
    def delete_files_gallery_view(self, delete):
        """delete file on gallery"""
        try:
            if delete == 'True':
                self.press_key('menu')
                #double press menu if menu is not there
                if not self.wait_for_ui_exists(400, text='Delete'):
                    self.press_key('menu')
                self.click_text('Delete')
                self.click_id('android:id/button1')
                return True
            else:
                return True
        except Exception, e:
            print Exception, ":", e
            return False
            
    def crash_watchers(self):
        self.d.watcher('AUTO_FC_WHEN_ANR').when(textMatches='.*is.*responding.*').click(resourceIdMatches='.*button1')
        self.d.watcher('Auto_FC_CRASH').when(textMatches='Unfortunately.*stopped.*').click(resourceIdMatches='.*button1')
        self.d.watchers.run()
    
    ### File manager handling  ####
    def open_file_manager(self):
        #Folder, Category
        #Storage information
        self.open_application('com.cloudminds.filemanager/.MainActivity')
        return self.wait_for_ui_exists(2000, packageName='com.cloudminds.filemanager')
    
    def filemanager_tab(self, tab):
        if tab == 'folder':
            self.click_text('Folder')
            return self.wait_for_ui_exists(2000, textMatches='Phone storage.*')
        else:
            self.click_text('Category')
            return self.wait_for_ui_exists(2000, text='Storage information')
    
    def filemanager_create_folder(self, folderName, storage='internal'):
        try:
            self.filemanager_tab('folder')
            self.click_ui(textMatches='Phone storage.*')
            time.sleep(0.3)
            self.press_key('menu')
            self.click_text('New folder')
            self.type_text(folderName, resourceIdMatches='.*text_ed')
            time.sleep(0.3)
            self.click_ui(resourceIdMatches='.*button1')
            return True
        except Exception, e:
            print Exception, ':', e
            return False
    
    def filemanager_check_file_exists(self, fileName):
        try:
            toFind = fileName+'.*'
            self.scroll_to_find(textMatches=toFind)
            return self.wait_for_ui_exists(1000, textMatches=toFind)
        except Exception, e:
            return False
            print Exception, ':', e
            
    def filemanager_delete_file(self, fileName):
        try:
            toFind = fileName+'.*'
            self.scroll_to_find(textMatches=toFind)
            self.long_click_ui(textMatches=toFind)
            self.click_ui(resourceIdMatches='.*action_delete')
            self.click_ui(resourceIdMatches='.*button1')
            return True
        except Exception, e:
            print Exception, ':', e
            return False
    
    ########################################################
    #           PIM
    #########################################################
    def open_callendar_app(self):
        """"""
        self.open_application('com.android.calendar/.AllInOneActivity')
        return self.wait_for_ui_exists(3000, resourceIdMatches='.*action_today')
    
    def create_callendar_events(self, title):
        self.calendar_main_window()
        self.click_ui(resourceIdMatches='.*floating_action_button')
        self.wait_for_ui_exists(2000, resourceIdMatches='.*title')
        self.type_text(title, resourceIdMatches='.*title')
        self.type_text('Wangjing SOHU A, Beijing, China', resourceIdMatches='.*location')
        self.click_text('Done')
    
    def check_callendar_events(self, title):
        self.calendar_main_window()
        self.press_key('menu')
        self.click_text('Delete events')
        return self.wait_for_ui_exists(3000, textContains=title)
    
    def delete_callendar_events(self):
        self.calendar_main_window()
        self.press_key('menu')
        self.click_text('Delete events')
        if self.wait_for_ui_exists(2000, resourceIdMatches='.*checkbox'):
            chkbox = self.d(resourceIdMatches='.*checkbox')
            for i in range(chkbox.count):
                self.click_ui(resourceIdMatches='.*checkbox', instance=i)
                
            self.click_ui(resourceIdMatches='.*action_delete')
            self.click_ui(resourceIdMatches='.*button1')
            return True
        else:
            return False
    
    def callendar_status(self):
        """
        0       --- Main window
        1       --- All events
        2       --- Create Events
        """
        if self.wait_for_ui_exists(300, resourceIdMatches='.*action_today'):
            return 0
        elif self.wait_for_ui_exists(300, text='All events'):
            return 1
        elif self.wait_for_ui_exists(300, resourceIdMatches='.*location'):
            return 2
    
    def calendar_main_window(self):
        status =self.callendar_status()
        if status == 0:
            return True
        elif status == 1:
            self.press_key('back')
        elif status == 2:
            self.press_key('back')
        else:
            self.press_key('back')
        return self.wait_for_ui_exists(300, resourceIdMatches='.*action_today')
        
    
if __name__ == "__main__":
    import sys
    p = UiKpiTest('0123456789ABCDEF')
    p.open_callendar_app()
    p.create_callendar_events('This is a callendar events')
    p.check_callendar_events('This is a callendar events')
    p.delete_callendar_events()
    #~ print p.open_file_manager()
    #~ print p.filemanager_create_folder('010')
    #~ print p.filemanager_check_file_exists('010')
    #~ print p.filemanager_delete_file('010')
    #~ print p.filemanager_check_file_exists('010')
    #p.crash_watchers()
    #print p.open_app_from_Home('Calendar', 'com.android.calendar')
    #p.open_application_from_Home('WPS Office', packageName='com.android.calendar')
    #p.test()
    #~ print p.open_camera_app()
    #~ p.capture_picture_video('still')
    #~ print p.open_file_from_camera('True')
    #~ p.goto_home()
    #~ print p.open_camera_app()
    #~ p.capture_picture_video('video')
    #~ print p.open_file_from_camera('True')
    #~ #print p.open_camera_mode('still')
    #~ #print p.open_camera_mode('video')
    #~ sys.exit()
    #~ print p.pause_music_playing()
    #~ print p.open_music_app()
    #~ print p.open_ongoing_music()
    #~ print p.play_next_music('5')
    
    
    #print p.play_music_shuffle_all()
    #print p.check_record_ui_status()
    #~ p.open_recorder_app()
    #~ print p.delete_record_files()
    #~ print p.record_voice(5)
    #~ print p.play_recorded_voice()
    #p.dial_number('10086')
    #p.wait_end_call()
    #p.add_new_contact("ABCD AAAA", "10086")
    #p.delete_contact("ABCD AAAA")
    #~ print p.open_message_app()
    #~ print p.open_message("This is MMS")
    #~ print p.forward_message('13910573271', 'This is MMS', 'True')
    #~ p.delete_msg_by_phoneNum("3271")
    #print p.open_browser_app()
    #print p.clear_browser_privacy()
    #print p.open_page()
    #print p.click_ui(textContains='139')
    #print p.verify_open('Browser', packageName='com.android.swe.browser')
    #print p.delete_file_in_downloads('weight.jpg')
    #print p.close_browser_app()
    #p.scroll_backward('horiz')