from tkinter import *
import tkinter.font as tkFont
from functools import partial
import time
import csv
from sklearn.mixture import GaussianMixture
import scipy.spatial.distance as dist 
import pandas as pd
import numpy as np
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

f = open(resource_path("log.txt"), "r")
x = f.read()
f.close()

press_time = scores = key_up_time = key_down_time1 = i = 0
is_released = True
access_denied_lab = wrong_pass = False
new_data = []
keys = []
key_values = {}
distance = []

top = Tk()

fontStyle = tkFont.Font(family="Lucida Grande", size=16)
input_txt = Entry(top, font=fontStyle)
input_txt.place(x = 610, y=230)

basic_info = Label(top, text="*if wrong key is pressed make sure to click the submit button to refresh the input box \n* On first instance the app requires 20 entries by the user \n* Then on next time the user will be required to enter the password for validation \n* Please make sure that capslock is off \n * Password entry is case-sensitive", font=fontStyle, fg="black")	
basic_info.place(x=400, y=700)
input_txt.focus()
def on_press(key):
	global is_released, key_down_time1, press_time, key_up_time
	if is_released:
		try: 
			if key.char in ['s','6','.','g','9','q','h','t']:
				keys.append(key.char)
				key_down_down_time = key_up_down_time = 0
				press_time = time.time()

				if key_down_time1 != 0:
					key_down_down_time = time.time() - key_down_time1 
					if key_down_down_time > 15.0:
						return False
					key_values[key.char+'_DD'] = float(key_down_down_time)
					print('keydown-keydown time {0}'.format(key_down_down_time))

				if key_up_time != 0:
					key_up_down_time = time.time() - key_up_time
					key_values[key.char+'_UD'] = float(key_up_down_time)
					print('keyup-keydown time {0}'.format(key_up_down_time))

				key_down_time1 = time.time()

		except AttributeError: 
			print('special key {0} pressed'.format(key))

		is_released = False

def on_release(key):
	global is_released, key_up_time, press_time
	if key.char in ['s','6','.','g','9','q','h','t']:

		hold_time = time.time() - press_time
		key_up_time = time.time()

		print('{0} released after {1}'.format(key, hold_time))
		key_values[key.char+'_Hold'] = float(hold_time)

			
	elif key.keysym == 27:
		top.destroy()
	is_released = True

def on_esc(key):
	top.destroy()

def password_entry(keys):
	global key_down_time1, press_time, key_up_time, i, wrong_pass,wrong_pass,wrong_password
	string = "".join(keys)
	press_time = key_down_time1 = key_up_time = 0
	is_released = True
	if wrong_pass:
		wrong_password.destroy()
		wrong_pass = False
	del keys[:]
	if string == 's6.g9qht':
		print("Password entry added")
		password_entry_approved = Label(top, text="Entry number "+str(i+1)+" submitted", font=fontStylewarning, fg="red")	
		password_entry_approved.place(x=570, y=100)
		print(key_values)
		# print("i value", i)
		if i == 0:
			with open(resource_path('key_data.csv'), 'w', newline='') as file:
				writer = csv.writer(file)
				writer.writerow(['s_Hold', '6_DD',  '6_UD', '6_Hold', '._DD', '._UD', '._Hold', 'g_DD',  'g_UD',  'g_Hold', '9_DD', '9_UD', '9_Hold',  'q_DD', 'q_UD', 'q_Hold', 'h_DD', 'h_UD', 'h_Hold', 't_DD', 't_UD', 't_Hold'])
				writer = csv.DictWriter(file, fieldnames = ['s_Hold', '6_DD',  '6_UD', '6_Hold', '._DD', '._UD', '._Hold', 'g_DD',  'g_UD',  'g_Hold', '9_DD', '9_UD', '9_Hold',  'q_DD', 'q_UD', 'q_Hold', 'h_DD', 'h_UD', 'h_Hold', 't_DD', 't_UD', 't_Hold'])
				writer.writerows([key_values])
		else:
			with open(resource_path('key_data.csv'), 'a+', newline='') as file:
				writer = csv.writer(file)
				writer = csv.DictWriter(file, fieldnames = ['s_Hold', '6_DD',  '6_UD', '6_Hold', '._DD', '._UD', '._Hold', 'g_DD',  'g_UD',  'g_Hold', '9_DD', '9_UD', '9_Hold',  'q_DD', 'q_UD', 'q_Hold', 'h_DD', 'h_UD', 'h_Hold', 't_DD', 't_UD', 't_Hold'])
				writer.writerows([key_values])
		i = i+1
	else:
		wrong_password = Label(top, text="Wrong Password,Please Re-enter", font=fontStylewarning, fg="red")	
		wrong_password.place(x=570, y=380)
		print("Wrong Password")
		wrong_pass = True
	input_txt.delete(0, "end")
	if i == 20:
		f = open(resource_path("log.txt"), "w")
		f.write("1")
		f.close()
		top.destroy()
	return True


def authorization_check(keys):
	global key_down_time1,press_time,key_up_time,scores,access_denied_lab,wrong_pass,wrong_password,access_denied
	string = "".join(keys)
	scores = press_time = key_down_time1 = key_up_time = 0
	is_released = True
	del new_data[:]
	del keys[:]
	input_txt.delete(0, "end")
	if access_denied_lab:
		access_denied.destroy()	
		access_denied_lab = False
	if wrong_pass:
		wrong_password.destroy()
		wrong_pass = False

	if string == 's6.g9qht':
		data = pd.read_csv(resource_path('key_data.csv'))
		train_data = data[['s_Hold', '6_DD',  '6_UD', '6_Hold', '._DD', '._UD', '._Hold', 'g_DD',  'g_UD',  'g_Hold', '9_DD', '9_UD', '9_Hold',  'q_DD', 'q_UD', 'q_Hold', 'h_DD', 'h_UD', 'h_Hold', 't_DD', 't_UD', 't_Hold']]

		for keys, values in key_values.items():
			new_data.append(values)

		gmm =  GaussianMixture(n_components=2, covariance_type='diag')
		gmm.fit(train_data)

		x = gmm.predict(np.array(new_data).reshape(-1,22))
		print("GMM",x[0])

		if x[0] == 1:
			scores += 1

		cb_distance = dist.cityblock(np.array(new_data).reshape(-1,22), train_data.mean())
		print("manhattan distance",cb_distance)
		if cb_distance < 1.4:
			scores += 1

		scaled_manhatten_distance = np.sum(np.true_divide(np.abs(np.subtract(np.array(new_data),train_data.mean())),train_data.mad()))
		print("Scaled manhanttan distance",scaled_manhatten_distance)
		if scaled_manhatten_distance < 50.0:
			scores += 1

		print("Scores",scores)
		if scores > 1:
			print("Access Granted")
			top.destroy()
			
		else:
			access_denied = Label(top, text="Access Denied !", font=fontStylewarning, fg="red")
			access_denied.place(x=630, y=380)
			print("Access Denied !")
			access_denied_lab = True
	else:	
		wrong_password = Label(top, text="Wrong Password,Please Re-enter", font=fontStylewarning, fg="red")	
		wrong_password.place(x=570, y=380)
		print("Wrong Password")
		wrong_pass = True

top.bind('<KeyPress>', on_press)
top.bind('<KeyRelease>', on_release)
top.bind('<Escape>', on_esc)

top.title("Keystroke Dynamics Authentication")

photo = PhotoImage(file = resource_path('icon.png'))
top.iconphoto(False, photo)
top.state("zoomed") 
top.resizable(0,0)
top.overrideredirect(1)

Label(top, text="Write Here \'s6.g9qht\' ", font=fontStyle).place(x=630, y=180)

fontStylewarning = tkFont.Font(family="Lucida Grande", size=20)
fontStylebtn = tkFont.Font(family="Lucida Grande", size=16)

def reset_button():
	f = open(resource_path("log.txt"), "w")
	f.write("0")
	f.close()
	top.destroy()

Button(top, text = "Reset",activebackground = "pink", activeforeground = "blue", font=fontStylebtn, command=reset_button).place(x =690, y = 820)  

if (x == '0'):
	if (i < 20):
		print("password_entry")
		sbmitbtn = Button(top, text = "Submit",activebackground = "pink", activeforeground = "blue", font=fontStylebtn, command=partial(password_entry,keys)).place(x =690, y = 260)  
		Label(top, text="Please input 20 values for the given password in free hand", font=fontStylewarning, fg="red").place(x=470, y=50)

else:
	print("authorization_check")
	sbmitbtn = Button(top, text = "Submit",activebackground = "pink", activeforeground = "blue", font=fontStylebtn, command=partial(authorization_check,keys)).place(x =690, y = 260)  
	Label(top, text="Input the given password for validation", font=fontStylewarning, fg="red").place(x=490, y=50)

top.mainloop()