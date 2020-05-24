#!/usr/bin/python3.8

from platform import system
import os

os.chdir(os.path.dirname(__file__))
os.chdir("..")
instagram_bot_folder_location = os.getcwd()


if (system() == "Linux") or (system() == "Darwin"):
    error_txt_file_address = instagram_bot_folder_location + "/error/"

elif system() == "Windows":
    error_txt_file_address = instagram_bot_folder_location + "\\error\\"



CHOOSING_USERNAME, GETTING_USERNAME, CHOOSING_PASSWORD, GETTING_PASSWORD, START_BUTTON, BUTTON_HANDLER = range(0, 6)

my_bot_token                     = '966866956:AAHafludOO9bviefKtMSkY8tNr2yMIgDnX4'


username_button_message          = """خب حالا میتونید با زدن دکمه 'نام کاربری' یوزر اینستاگرام خود را وارد کنید\n\nWell, now you can enter your Instagram user by clicking the 'username' button"""


input_username_message           = "نام کاربری خود را وارد کنید:\n\nEnter your username:"


input_password_message           = "پسورد خود را وارد کنید:\n\n\n\nEnter your password:"


password_button_message          = "روی گزینه رمز عبور کلیک کنید در صورتی که فک می کنید نام کاربری خود را اشتباه وارد کردید روی دکمه مرحله قبل کلیک کنید\n\nClick on the password option. If you think you entered your username incorrectly, click the previous step button."


start_button_message             = "روی گزینه شروع فعالیت کلیک کنید در صورتی که فک می کنید نام کاربری و یا پسورد یا هردو را اشتباه وارد کردید روی دکمه مرحله قبل کلیک کنید\n\nClick on the Start option if you think you entered the wrong username or password or both, click the button on the previous step."


waiting_message                  = "من منتظرم که شما یه گزینه ای رو انتخاب کنید\n\nI'm waiting for you to choose an option"


choose_option_message            = "بین گزینه های زیر انتخاب کنید:\n\nChoose from the following options:"


start_activity_message           = "حله در حال حاضر می تونم فقط این چندتا قابلیت رو در اختیارتون بزارم البته بعدها با توجه به نظر شما کاربرا بیشتر میشن حالا با توجه به نکاتی که گفتم روی چیزی که میخوای کلیک کن و اگه همچنان فکر میکنی که نام کاربری و پسوردت رو اشتباه زدی روی دکمه شروع دوباره بزن تا همه چی از سر گرفته بشه\n\nNow, I can only give you these few features, but later, according to your opinion, the number of those will be increase. Now, according to the points I said, click on what you want, and if you still think that you have mistaken your username and password. Click the Start again to restart everything"


warning_to_click_unfollow_button = """شما در ابتدای فعالیت خود نمیتوانید از قابلیت آنفالو استفاده کنید ابتدا شروع به فعالیت با گزینه های فالو یا حالت خودکار و سپس تکمیل فرایند خود کنید و یا می توانید به صورت دستی با زدن روی آخرین گزینه ربات لینک کسایی که شمارا آنفالو کردند به دست بیاورید و خودتان شروع به آنفالو کنید\n\nYou can't use the unfollow feature at the beginning of your activity, first start with the follow or auto mode options and then complete your process, or you can manually click on the last option to get the links who unfollowed you. And start to unfollow them yourself"""

warning_to_unfollow_persons     = """تذکر:\n۱- اگر می خواهید امروز فقط آنفالو انجام دهید سعی کنید بین 7 تا 10 آنفالو در ساعت انجام دهید\n۲- اگر می خواهید امروز فعالیت های دیگر هم علاوه بر آنفالو داشته باشید کمتر از 100 نفر آنفالو کنید و بقیه کار رو با انتخاب یک گزینه ی دیگه به ربات بسپارید\n\nNote:\n1- If you want to do only unfollow today, try to do between 7 and 10 unfollow per hour.\n2- If you want to have other activities in addition to unfollow today, do less than 100 people and do the rest by choosing. Leave another option to the robot"""


login_error_message              = "مثل اینکه شما در هنگام ورود به اکانت خود به مشکل خوردید گزینه های زیر را چک کنید:\n\n۱- چک کنید که پسورد و نام کاربری شما حتما درست باشد\n\n۲- اتصال خود را به اینترنت بررسی کنید\n\n۳- اگر با صفحه احراز هویت اینستاگرام رو به رو شدید باید هویت خود را دستی تایید کنید و بعد ربات را اجرا کنید\n\n۴- در صورتی که این گزینه ها را چک کردید و هیچ کدام از آنها مشکل شما را برطرف نکرد به یوزر سازنده ربات که در بایو قرار دارد پیام دهید تا مشکل بررسی شود\n\nIt's as if you had trouble logging in to your account.Check the following options:\n1. Make sure your password and username are correct.\n2. Check your Internet connection.\n3. If you have an Instagram authentication page. You have to verify your identity manually and then run the robot.\n4- If you checked these options and none of them solved your problem, send a message to the robot user user in the bio to solve the problem. Review"


start_command_message            = """سلام به اولترانگرام خوش اومدید قبل از شروع فعالیتتون بهتره که نکاتی رو خدمتتون عرض کنم و حتما همه نکات گفته شده رو با دقت مطالعه کنید:\n\n۱-  این ربات تازه درست شده پس خواهشی که دارم اینه که انتظاراتتون رو مقداری اگه میشه پایین بیارید و حمایت کنید این ربات رو تا در راستای بهتر شدن ربات به شما کاربرای عزیر کمک کنم\n\n۲-  حواستون باشه که من بین بعضی فعالیت ها 24 ساعت وقفه قرار دادم پس اگه میخواین فعالیتی انجام بدین نوع فعالیت خودتون رو بین گزینه ها با احتیاط انتخاب کنید چون بعدش تا 24 ساعت بعد به بعضی فعالیت ها دسترسی ندارین در واقع فقط در روز می توانید از یک قابلیت ربات استفاده کنید این محدودیت و محدودیت های دیگه ربات در اجرا فقط بخاطر وجود محدودیت های اینستاگرام و رصد شدن فعالیت های ربات گونه توسط الگوریتم های اینستاگرام هستش و سعی شده که با این محدودیت ها از بلاک شدن اکانت شما و تشخیص فعالیت های ربات گونه توسط اینستاگرام جلوگیری بشه\n\n۳-  اگه با ربات مشکلی داشتین از طریق یوزری که در بایو ربات قرار دادم می تونید مشکل رو به من اطلاع رسانی کنید تا حلش کنم\n\n۴-  با زدن روی دکمه شروع دوباره می توانید فعالیت خود را از سر بگیرید\n\n۵-  متاسفانه ربات رو فقط روی کامپیوتر یا لپ تاپ می تونید اجرا کنید و امکان اجرا روی گوشی در حال حاضر وجود نداره\n\n۶-  توی لپ تاپ یا کامپیوتر شما برای اجرای ربات نیاز به مرورگر دارید و پیشنهاد میشه که حتما از مرورگر موزیلا یا همون فایرفاکس استفاده کنید\n\n۷-  در اخرم که مخلص همه کاربرای جدید هستم و به خصوص کسایی که قراره حمایت کنن این ربات رو و امیدوارم که بتونم توجه و اطمینان شما کاربرای عزیز و دوست داشتنی رو به این ربات جلب کنم\n\n\nHello, welcome to Ultrongram. Before starting your activity, it is better for me to offer you some tips, and be sure to read all the above points carefully:\n\n1- This new robot has been created, so my request is that you lower your expectations a bit. Bring and support this robot to help you improve the robot for you\n\n2- Be aware that I put a 24 hour interval between some activities, so if you want to do something put your activity among the options.Choose carefully because you will not have access to some activities until 24 hours later. In fact, you can only use one robot feature per day. This limitation and other limitations of the robot in execution are only due to Instagram restrictions and monitoring of robot activities. The cheek is by Instagram algorithms and it has been tried with these restrictions to prevent your account from being blocked and Instagram to recognize the robot's activities. \n\n3- Let me know the problem so I can fix it\n\n4- Click the start button ,you can resume your activity\n \n5- Unfortunately, you can run the robot only on your computer or laptop, and it is not possible to run it on your phone at the moment.\n\n6- In your laptop or computer to run it You need a browser and it is recommended that you use the Mozilla browser or Firefox\n\n7- In the end, I am sincere to all new users, especially those who are going to support this robot, and I hope I can draw your attention and confidence. Dear and lovable user, I would like to draw attention to this robot"""


runtime_error_message             = """به دلایلی انگار که ربات متوقف شده و مثل اینکه در اجرای دستور شما به مشکل خورده با زدن گزینه شروع دوباره فرایند اجرای فعالیت را از سر بگیرید و اگر با چند بار اجرا کردن مشکل برطرف نشد این مشکل رو به سازنده من گزارش بدید\n\nFor some reason, it seems that the robot has stopped and, as if it had a problem executing your command, start the process again by tapping the start option, and if the problem is not solved by running it a few times, report this problem to my developer."""


error_message_to_execute_command  = "من نمی تونم توی این مرحله یک دستور به طور مثال /start رو اجرا کنم\n\nI can't run a command, for example /start, at this point"


connection_error_message          = 'به دلیل قطع شدن اتصال شما به اینترنت در هنگام ورود به اکانتتون فعالیت مورد نظر لغو شد می توانید دوباره فعالیت خود را آغاز کنید\n\nYou can resume your activity due to the disconnection of your Internet connection when you log in to your account.'


successfully_message              = "عملیات شما با موفقیت انجام شد\n\nYour operation was successful"


close_driver_error_message        = "لطفا در در هنگام اجرای ربات مرورگر را نبندید (روی ضربدر پنجره مرورگر کلیک نکنید) و بزارید ربات رو حالت اجرا بماند\n\nPlease do not close the browser when running the robot (do not click on the browser window) and let the robot run."


error_message_for_browers         = "شما باید مرورگر فایرفاکس را اول نصب کنید\n\nYou must first install the Firefox browser"


error_message_for_oprating_system = "سیستم عامل شما مورد قبول نیست\n\nYour operating system is not acceptable"





def get24HourMessage(last_run_time, passed_time):
    message = f"باید از آخرین فعالیت شما 24 بگذرد آخرین فعالیت شما در ساعت {last_run_time} ثبت شده است و زمان گذشته شده از آخرین فعالیت شما {passed_time} می باشد\n\nنکته:\nدقت کنید که اگر می خواهید از قابلیت آنفالو استفاده کنید باید بین هر بار استفاده از این  قابلیت 7 روز یا بیشتر و نسبت به قابلیت های دیگر هم 1 روز یا بیشتر فاصله وجود داشته باشد\n\n\nIt should be 24 hours from your last activity\nYour last activity was recorded at {last_run_time} and the time elapsed since your last activity is {passed_time}\n\nNote:\nThere should be a 7 day or more away from unfollow features and a day or more away from other features"
    
    return message

def get7dayMessage(last_run_time, passed_time_in_day, passed_time_in_hour):
    massage = f"""باید از اخرین زمان استفاده شما از قابلیت آنفالو 7 روز یا بیشتر و نسبت به قابلیت های دیگر 1 روز یا بیشتر بگذرد اخرین زمان استفاده شما از قابلیت آنفالو در ساعت {last_run_time} می باشد زمان گذشته از اخرین فعالیت شما {passed_time_in_day} روز و {passed_time_in_hour} است\n\n\nIt should take 7 days or more from the last time you use the Anfal feature and 1 day or more from other features The last time you use unfollow features is at {last_run_time} The last time of your last activity is {passed_time_in_day} day and {passed_time_in_hour}"""

    return massage






