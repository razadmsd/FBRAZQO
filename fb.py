import os
import sys
import time
import random
import string
import getpass
import socket
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs
from faker import Faker
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.prompt import Prompt, IntPrompt
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()

locales = ['id_ID', 'en_US']
faker = Faker(random.choice(locales))
ua = UserAgent()

TEMP_DOMAINS_LIST = ['@tempmail.com', '@mailinator.com', '@tempmail.net', 
                     '@guerrillamail.com', '@throwawaymail.com', '@10minutemail.com', 
                     '@temp-mail.org', '@trashmail.com', '@temporarymail.com', 
                     '@mailnesia.com', '@dispostable.com', '@getnada.com', 
                     '@inboxkitten.com', '@spam4.me', '@moakt.cc', '@mytemp.email', 
                     '@fakemail.net', '@fakeinbox.com', '@shitmail.me', '@spamgourmet.com', 
                     '@burnermail.io', '@spamdecoy.net', '@spambox.us', '@letthemeatspam.com', 
                     '@guerillamail.org', '@mailtemp.net', '@spaml.de', '@deadaddress.com', 
                     '@spamthisplease.com', '@nowmymail.com', '@tempinbox.com', 
                     '@trashmail.se', '@mail1a.de', '@emailondeck.com', '@tempcloud.info', 
                     '@dudmail.com', '@spamrol.com', '@yopmail.com', '@yopmail.fr', 
                     '@yopmail.net', '@mvrht.com', '@oweiidfjj.com', '@emailll.org', 
                     '@labelmail.xyz', '@insta-mail.de', '@budaya-ptic.com', '@muxi.com', 
                     '@april.biz', '@tmails.net', '@cuoly.com', '@pwrby.com', 
                     '@digital-mail.net', '@hax0r.id', '@vibe.com', '@emailll.net', 
                     '@tempsky.com', '@mihci.com', '@jmail.ovh', '@throwam.com', 
                     '@dropmail.me', '@tempmailer.com', '@nowemail.org', '@spam-be-gone.com', 
                     '@inboxbear.com', '@temppostmail.com', '@inboxed.net', '@trashworld.net', 
                     '@mailsac.com', '@tempomail.fr', '@templo.cc', '@boximail.com', 
                     '@rapidmail.xyz', '@kappala.net', '@mytrashmail.com', '@spamkill.com', 
                     '@crapmail.de', '@no-spam.ws', '@swift-mail.me', '@zippymail.info', 
                     '@tempm.com', '@0wnd.net', '@pidmail.com', '@ftmail.com', 
                     '@unixmail.pro', '@automail.net', '@anonbox.net', '@boxtemp.com', 
                     '@nobulk.com', '@luxusmail.org', '@luxusmail.io', '@fexbox.org', 
                     '@webe.men', '@inboxify.me', '@my10minmail.com', '@sharklasers.com', 
                     '@grr.la', '@pokemail.net', '@p33.org', '@hackermail.com', 
                     '@disposablemail.com', '@mailnull.com', '@soodonims.com', 
                     '@fakemail.net', '@lroid.com', '@crazymail.info', '@temp1mail.com', 
                     '@spamfree24.de', '@spamfree24.org', '@spamfree24.info', '@spamfree24.eu', 
                     '@mailnesia.uk', '@maildrop.cc', '@spambox.xyz', '@spammail.org', 
                     '@temp-mail.io', '@temp-mail.cc', '@emkei.cz', '@tempgmail.com', 
                     '@emailtoyou.net', '@mailzi.ru', '@mailezee.net', '@p33.me', 
                     '@inboxbox.org', '@trashmail.com', '@spambox.email']

REAL_DOMAINS_LIST = ['@gmail.com', '@yahoo.com', '@outlook.com', '@hotmail.com', 
                     '@proton.me', '@icloud.com', '@aol.com', '@mail.com', '@gmx.com', 
                     '@live.com', '@msn.com', '@ymail.com', '@inbox.com', '@fastmail.com', 
                     '@tuta.io', '@zoho.com', '@hey.com', '@hushmail.com', '@yandex.com', 
                     '@qq.com', '@163.com', '@126.com', '@sina.com', '@protonmail.com', 
                     '@rediffmail.com', '@libero.it', '@web.de', '@freenet.de', '@mail.ru', 
                     '@naver.com', '@daum.net', '@cox.net', '@verizon.net', '@shaw.ca', 
                     '@rogers.com', '@bellsouth.net', '@earthlink.net', '@btinternet.com', 
                     '@sky.com', '@orange.fr', '@wanadoo.fr', '@laposte.net', '@sfr.fr', 
                     '@virgilio.it', '@alice.it', '@tiscali.it', '@seznam.cz', '@centrum.cz', 
                     '@atlas.cz', '@mail.dk', '@mail.ee', '@onmail.com', '@safe-mail.net', 
                     '@usa.com', '@iname.com', '@europe.com', '@asia.com', '@mailfence.com', 
                     '@cleanmail.net', '@swissmail.org', '@onet.pl', '@op.pl', '@wp.pl', 
                     '@o2.pl', '@interia.pl', '@bigpond.com', '@optusnet.com.au', '@xtra.co.nz', 
                     '@zoznam.sk', '@post.sk', '@bol.com.br', '@uol.com.br', '@terra.com.br', 
                     '@ig.com.br', '@r7.com', '@bol.com', '@gmx.net', '@live.co.uk', 
                     '@hotmail.co.uk', '@rocketmail.com', '@hotmail.fr', '@hotmail.de', 
                     '@outlook.fr', '@outlook.de', '@live.fr', '@live.de', '@mac.com', 
                     '@me.com', '@blueyonder.co.uk', '@talktalk.net', '@ntlworld.com', 
                     '@virginmedia.com', '@btopenworld.com', '@eircom.net', '@mail2world.com', 
                     '@lavabit.com', '@t-online.de', '@t-email.hu', '@telefonica.net', 
                     '@arcor.de', '@charter.net', '@frontier.com', '@sbcglobal.net', 
                     '@bellsouth.net', '@iname.com', '@inbox.lv', '@ptd.net', '@twc.com', 
                     '@embarqmail.com', '@centurylink.net', '@windstream.net', '@mail2web.com', 
                     '@greennet.org.uk', '@riseup.net', '@tutamail.com', '@keemail.me', 
                     '@posteo.net', '@mailbox.org', '@selfhost.de', '@webmail.co.za', 
                     '@telkomsa.net', '@vodamail.co.za', '@163.net', '@126.net', '@hotmail.it', 
                     '@hotmail.es', '@outlook.es', '@live.es', '@live.it']

status = {'live': 0, 'cp': 0, 'loop': 0}
settings = {
    'limit': 1,
    'password': 'RAZQO',
    'use_temp_email': False,
    'use_real_email': False,
    'gmail_only': False,
    'use_file_email': False
}

SAVE_DIR = Path('/sdcard/FACEBOOKME')
SAVE_DIR.mkdir(parents=True, exist_ok=True)
SAVE_FILE = SAVE_DIR / 'hasilakun.txt'

MAX_WORKERS = 6
DELAY_RANGE = (1.2, 2.5)

HEADER_CACHE = {'total_live': 0, 'loaded': False}

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return 'Tidak dapat mengambil IP'

samsung_devices = [
    ('SM-G991B', 'Galaxy S21'), ('SM-G996B', 'Galaxy S21+'), ('SM-G998B', 'Galaxy S21 Ultra'),
    ('SM-G990E', 'Galaxy S21 FE'), ('SM-G973F', 'Galaxy S10'), ('SM-G975F', 'Galaxy S10+'),
    ('SM-G970F', 'Galaxy S10e'), ('SM-G965F', 'Galaxy S9+'), ('SM-G960F', 'Galaxy S9'),
    ('SM-G955F', 'Galaxy S8+'), ('SM-G950F', 'Galaxy S8'), ('SM-G935F', 'Galaxy S7 Edge'),
    ('SM-G930F', 'Galaxy S7'), ('SM-G925F', 'Galaxy S6 Edge'), ('SM-G920F', 'Galaxy S6'),
    ('SM-N986B', 'Galaxy Note 20 Ultra'), ('SM-N981B', 'Galaxy Note 20'), ('SM-N975F', 'Galaxy Note 10+'),
    ('SM-N970F', 'Galaxy Note 10'), ('SM-N960F', 'Galaxy Note 9'), ('SM-N950F', 'Galaxy Note 8'),
    ('SM-N920C', 'Galaxy Note 5'), ('SM-N910C', 'Galaxy Note 4'), ('SM-A736B', 'Galaxy A73'),
    ('SM-A725F', 'Galaxy A72'), ('SM-A715F', 'Galaxy A71'), ('SM-A556E', 'Galaxy A55'),
    ('SM-A546E', 'Galaxy A54'), ('SM-A536E', 'Galaxy A53'), ('SM-A526B', 'Galaxy A52 5G'),
    ('SM-A525F', 'Galaxy A52'), ('SM-A516F', 'Galaxy A51'), ('SM-A515F', 'Galaxy A51'),
    ('SM-A505F', 'Galaxy A50'), ('SM-A325F', 'Galaxy A32'), ('SM-A315F', 'Galaxy A31'),
    ('SM-A217F', 'Galaxy A21s'), ('SM-A127F', 'Galaxy A12'), ('SM-A115F', 'Galaxy A11'),
    ('SM-A022F', 'Galaxy A02s'), ('SM-A013F', 'Galaxy A01'), ('SM-M546B', 'Galaxy M54'),
    ('SM-M526B', 'Galaxy M52'), ('SM-M515F', 'Galaxy M51'), ('SM-M315F', 'Galaxy M31'),
    ('SM-M215F', 'Galaxy M21'), ('SM-M127F', 'Galaxy M12'), ('SM-M115F', 'Galaxy M11'),
    ('SM-J710F', 'Galaxy J7'), ('SM-J700F', 'Galaxy J7'), ('SM-J530G', 'Galaxy J5'),
    ('SM-J510G', 'Galaxy J5'), ('SM-J330G', 'Galaxy J3'), ('SM-J320G', 'Galaxy J3')
]

xiaomi_devices = [
    ('M2011K2G', 'Mi 11'), ('M2102K1AC', 'Mi 11 Ultra'), ('M2101K9C', 'Mi 11 Lite'),
    ('M1902F1G', 'Mi 9'), ('M1803E1A', 'Mi 8'), ('2312DRA50G', 'Redmi Note 13'),
    ('23021RAAEG', 'Redmi Note 12'), ('2201116SG', 'Redmi Note 11'), ('M2102J20SG', 'Redmi Note 10'),
    ('M2101K6G', 'Redmi Note 10 Pro'), ('M2003J15SC', 'Redmi Note 9'), ('M1903C3GG', 'Redmi Note 8'),
    ('M1803E7SG', 'Redmi Note 7'), ('22101320G', 'Redmi 12'), ('M2101K9G', 'Redmi 10'),
    ('M2006C3MG', 'Redmi 9A'), ('M2010J19CG', 'Redmi 9'), ('M1908C3IG', 'Redmi 8'),
    ('M1908C3JG', 'Redmi 8A'), ('23049PCD8G', 'Poco X5 Pro'), ('22041216G', 'Poco X5'),
    ('M2102K1G', 'Poco X3 Pro'), ('M2101K7AG', 'Poco X3'), ('M2007J20CG', 'Poco M3'),
    ('M2006C3MI', 'Poco C3')
]

android_versions = ['9', '10', '11', '12', '13', '14']
locales = ['en-US', 'en-GB', 'id-ID']

def chrome_version():
    return f"{random.randint(110, 124)}.0.{random.randint(5000, 7000)}.{random.randint(50, 200)}"

def samsung_browser_version():
    return f"{random.randint(20, 23)}.0"

def firefox_version():
    v = random.randint(109, 124)
    return f"{v}.0"

def edge_version():
    return f"{random.randint(110, 124)}.0.{random.randint(1500, 2500)}.{random.randint(50, 200)}"

def opera_version():
    return f"{random.randint(70, 80)}.0.{random.randint(3500, 4500)}.{random.randint(50, 200)}"

def generate_user_agent():
    brand = random.choice(['Samsung', 'Xiaomi'])
    
    if brand == 'Samsung':
        model, _ = random.choice(samsung_devices)
    else:
        model, _ = random.choice(xiaomi_devices)
    
    android = random.choice(android_versions)
    locale = random.choice(locales)
    browser = random.choice(['chrome', 'samsung', 'firefox', 'edge', 'opera', 'webview'])
    
    if browser == 'chrome':
        return f"Mozilla/5.0 (Linux; Android {android}; {model}; {locale}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version()} Mobile Safari/537.36"
    elif browser == 'samsung':
        return f"Mozilla/5.0 (Linux; Android {android}; {model}; {locale}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{samsung_browser_version()} Chrome/{chrome_version()} Mobile Safari/537.36"
    elif browser == 'firefox':
        v = firefox_version()
        return f"Mozilla/5.0 (Android {android}; Mobile; rv:{v}; {model}) Gecko/{v} Firefox/{v}"
    elif browser == 'edge':
        return f"Mozilla/5.0 (Linux; Android {android}; {model}; {locale}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version()} Mobile Safari/537.36 EdgA/{edge_version()}"
    elif browser == 'opera':
        return f"Mozilla/5.0 (Linux; Android {android}; {model}; {locale}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version()} Mobile Safari/537.36 OPR/{opera_version()}"
    else:  # webview
        return f"Mozilla/5.0 (Linux; Android {android}; {model}; {locale}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{chrome_version()} Mobile Safari/537.36"

def extract_form(html):
    keys = ['lsd', 'jazoest', 'fb_dtsg', 'reg_instance', 'reg_impression_id', 'logger_id']
    data = {}
    
    for key in keys:
        found = re.search(f'name="{key}" value="(.*?)"', html)
        if found:
            data[key] = found.group(1)
    
    return data

email_list_from_file = []

def load_email_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
        
        if not emails:
            console.print('[red]File kosong![/red]')
            return False
        
        global email_list_from_file
        email_list_from_file = emails[:]
        
        console.print(f'[green]Total email dimuat: {len(email_list_from_file)}[green]')
        return True
    except Exception as e:
        console.print(f'[red]Terjadi kesalahan saat membaca file: {e}[/red]')
        return False

def manual():
    console.print('[bold white]Isi file email satu per baris[bold white]')
    path = Prompt.ask('[bold white]Masukkan path file email[bold white]').strip()
    
    if not path:
        console.print('[yellow]Path kosong, dibatalkan.[yellow]')
        return
    
    ok = load_email_file(path)
    if ok:
        settings['use_file_email'] = True
        settings['use_temp_email'] = False
        settings['use_real_email'] = False
        settings['gmail_only'] = False
        console.print('[green]Mode email dari file AKTIF[green]')
    else:
        settings['use_file_email'] = False

def get_email():
    if settings.get('use_file_email'):
        if email_list_from_file:
            return email_list_from_file.pop(0)
        else:
            console.print('[yellow]Email dari file habis — beralih ke mode lain (jika ada).[/yellow]')
            settings['use_file_email'] = False
    
    if settings.get('gmail_only'):
        return f"{faker.first_name().lower()}{faker.last_name().lower()}{random.randint(1000, 9999)}@gmail.com"
    
    if settings.get('use_temp_email'):
        return f"{faker.first_name().lower()}{faker.last_name().lower()}{random.randint(10, 999)}{random.choice(TEMP_DOMAINS_LIST)}"
    
    if settings.get('use_real_email'):
        return f"{faker.first_name().lower()}{faker.last_name().lower()}{random.randint(100, 999)}{random.choice(REAL_DOMAINS_LIST)}"
    
    # Default: generate phone number (Indonesia)
    prefix_list = ['0811', '0812', '0813', '0821', '0822', '0823', '0852', '0853', 
                   '0851', '0814', '0815', '0816', '0855', '0856', '0857', '0858', 
                   '0817', '0818', '0819', '0859', '0877', '0878', '0895', '0896', 
                   '0897', '0898', '0899', '0881', '0882', '0883', '0884', '0885', 
                   '0886', '0887', '0888', '0889']
    
    prefix = random.choice(prefix_list)
    number_length = random.choice([7, 8, 9])
    
    return prefix + ''.join(random.choice('0123456789') for _ in range(number_length))

def get_facebook_profile_info(uid):
    try:
        url = f'https://www.facebook.com/{uid}'
        r = requests.get(url, timeout=10)
        
        if r.status_code != 200:
            return 'Profil tidak dapat diakses'
        
        soup = bs(r.text, 'html.parser')
        title_tag = soup.find('title')
        
        if not title_tag:
            return 'Nama tidak ditemukan'
        
        title = title_tag.text.strip()
        if not title or 'facebook' in title.lower():
            return 'Nama tidak ditemukan'
        
        return title
    except requests.exceptions.RequestException:
        return 'Error saat mengakses profil'
    except Exception:
        return 'Error tidak diketahui'

def check_uid(uid):
    try:
        headers = {
            'User-Agent': generate_user_agent(),
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8',
            'Accept': 'text/html,application/xhtml+xml',
            'Connection': 'keep-alive'
        }
        
        url = f'https://m.facebook.com/{uid}'
        r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if r.status_code != 200 or not r.text:
            return None
        
        html = r.text.lower()
        
        block_keywords = ['login', 'masuk', 'checkpoint', 'security check', 
                         'not found', 'konten tidak ditemukan', 
                         "page isn't available", 'you must log in']
        
        for word in block_keywords:
            if word in html:
                return None
        
        soup = bs(r.text, 'html.parser')
        
        og = soup.find('meta', property='og:title')
        if og and og.get('content'):
            name = og['content'].strip()
        else:
            title = soup.find('title')
            if not title:
                return None
            name = title.text.strip()
        
        blacklist_title = ['facebook', 'log into facebook', 'masuk ke facebook', 
                          'checkpoint', 'error', 'not found']
        
        for bad in blacklist_title:
            if bad in name.lower():
                return None
        
        if len(name) < 3 or len(name) > 80:
            return None
        
        return {'uid': uid, 'name': name}
    except:
        return None

NICKNAME_FILE = 'nickname.txt'

def get_nickname():
    if os.path.exists(NICKNAME_FILE):
        try:
            with open(NICKNAME_FILE, 'r') as f:
                nickname = f.read().strip()
                if nickname:
                    return nickname.upper()
        except:
            pass
    
    while True:
        nickname = input('Masukkan Nama Anda : ').strip()
        
        if not nickname:
            print('Nama tidak boleh kosong!')
            continue
        
        if not re.fullmatch('[A-Za-z]+', nickname):
            print('Nama hanya boleh huruf (A-Z)!')
            continue
        
        nickname = nickname.upper()
        
        try:
            with open(NICKNAME_FILE, 'w') as f:
                f.write(nickname)
        except:
            pass
        
        return nickname

def register_account():
    status['loop'] += 1
    
    for i in range(2, 0, -1):
        console.print(f'[grey50]──> ([green]Waktu-> {i}s Akun-> {status["loop"]}[grey50]) — ([green]Success:[green]{status["live"]} [grey50]/ [red]Check:[red]{status["cp"]}[grey50])', end='\r')
        sys.stdout.flush()
        time.sleep(1)
    
    try:
        ses = requests.Session()
        res = ses.get('https://touch.facebook.com/reg')
        form = extract_form(res.text)
        
        fname = faker.first_name().lower() + ' ' + faker.last_name().lower()
        lname = faker.last_name().lower()
        email = get_email()
        password = settings['password']
        
        birth_day = f"{random.randint(1, 28):02d}"
        birth_month = f"{random.randint(1, 12):02d}"
        birth_year = str(random.randint(1980, 2000))
        gender_code = random.choice(['1', '2'])
        gender_text = 'Perempuan' if gender_code == '1' else 'Laki-laki'
        
        payload = {
            'lsd': form.get('lsd', ''),
            'jazoest': form.get('jazoest', ''),
            'fb_dtsg': form.get('fb_dtsg', ''),
            'reg_instance': form.get('reg_instance', ''),
            'reg_impression_id': form.get('reg_impression_id', ''),
            'logger_id': form.get('logger_id', ''),
            'firstname': fname,
            'lastname': lname,
            'birthday_day': birth_day,
            'birthday_month': birth_month,
            'birthday_year': birth_year,
            'sex': gender_code,
            'reg_email__': email,
            'reg_passwd__': password,
            'encpass': f'#PWD_BROWSER:0:{int(time.time())}:{password}',
            'submit': 'Daftar',
            '__dyn': '',
            '__csr': '',
            '__req': 'q',
            '__a': '1',
            '__user': '0'
        }
        
        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8", "Google Chrome";v="105"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': generate_user_agent(),
            'viewport-width': '980',
            'referer': 'https://m.facebook.com/login/save-device/',
            'dpr': '2'
        }
        
        reg = ses.post('https://limited.facebook.com/reg/submit/', data=payload, headers=headers)
        cookies = ses.cookies.get_dict()
        
        if 'c_user' in cookies:
            uid = cookies['c_user']
            cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            profile_name = get_facebook_profile_info(uid)
            
            if profile_name and 'Facebook' not in profile_name:
                status['live'] += 1
                HEADER_CACHE['total_live'] += 1
                
                created_date = datetime.now().strftime('%d-%m-%Y')
                tgl_lahir = f"{birth_day}-{birth_month}-{birth_year}"
                
                from rich.tree import Tree
                tree = Tree(f'[bold green]Akun Berhasil Dibuat — UID [green]{uid}[green][bold green]')
                akun = tree.add('[cyan]Informasi Akun Lengkap[cyan]')
                akun.add(f'[bold white]Nama Lengkap[/]: [bold green]{profile_name}[/]')
                akun.add(f'[bold white]UID[/]: [bold green]{uid}[/]')
                akun.add(f'[bold white]Password[/]: [bold green]{password}[/]')
                akun.add(f'[bold white]Email/Nomor[/]: [bold green]{email}[/]')
                akun.add(f'[bold white]Jenis Kelamin[/]: [bold green]{gender_text}[/]')
                akun.add(f'[bold white]Tanggal Lahir[/]: [bold green]{tgl_lahir}[/]')
                akun.add(f'[bold white]Tanggal Akun Dibuat[/]: [bold green]{created_date}[/]')
                akun.add(f'[bold white]Cookie[/]: [bold green]{cookie_str}[/]')
                
                console.print(Panel(tree, title='[green]SUCCESS[green]'))
                
                with open(SAVE_FILE, 'a', encoding='utf-8') as f:
                    f.write(f'{uid}|{password}|{cookie_str}\n')
        else:
            status['cp'] += 1
        
        time.sleep(random.uniform(5, 10))
    except requests.exceptions.RequestException:
        time.sleep(random.uniform(5, 10))
    except Exception:
        time.sleep(random.uniform(5, 10))

def count_total_live_from_folder(folder: Path) -> int:
    total = 0
    if not folder.exists():
        return 0
    
    for file in folder.glob('*.txt'):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if '|' not in line:
                        continue
                    
                    uid = line.split('|', 1)[0]
                    if uid.isdigit():
                        total += 1
        except:
            continue
    
    return total

def load_header_once():
    if HEADER_CACHE['loaded']:
        return
    
    HEADER_CACHE['total_live'] = count_total_live_from_folder(SAVE_DIR)
    HEADER_CACHE['loaded'] = True

def show_header_once():
    load_header_once()
    
    panel_content = f"""[bold white]Total Live (Folder): [bold green]{HEADER_CACHE['total_live']}[/]
[bold white]Folder Result    : [bold green]{SAVE_DIR}[/]
[bold white]Facebook Account Creator[/]"""
    
    console.print(Panel(panel_content, title='FACEBOOK CREATE', subtitle='Auto Creator'))

def show_menu_once():
    menu_text = f"""[bold white] (01). Mulai Create[bold white]
[bold white] (02). Set Limit Create[bold white]
[bold white] (03). Set Password[bold white]
[bold white] (04). Temp Mail           : [bold cyan]{'ON' if settings['use_temp_email'] else 'OFF'}[bold cyan]
[bold white] (05). Real Email          : [bold cyan]{'ON' if settings['use_real_email'] else 'OFF'}[bold cyan]
[bold white] (06). Gmail Only          : [bold cyan]{'ON' if settings['gmail_only'] else 'OFF'}[bold cyan]
[bold white] (07). Cek UID Tersimpan[bold white]
[bold white] (08). File Email          : [bold cyan]{'ON' if settings['use_file_email'] else 'OFF'}[bold cyan]
[bold white] (00). Keluar[bold white]"""
    
    console.print(Panel(menu_text, title='[bold yellow] MENU UTAMA [bold yellow]', border_style='bold white', width=60))

def menu():
    while True:
        clear_screen()
        show_header_once()
        show_menu_once()
        
        try:
            choice = Prompt.ask('Pilih', choices=[str(i) for i in range(10)], default='1')
            
            if choice == '1':
                start_create_accounts()
            elif choice == '2':
                set_limit()
            elif choice == '3':
                set_password()
            elif choice == '4':
                toggle_temp_email()
            elif choice == '5':
                toggle_real_email()
            elif choice == '6':
                toggle_gmail_only()
            elif choice == '7':
                check_saved_uid()
            elif choice == '8':
                toggle_file_email()
                if settings.get('use_file_email'):
                    manual()
                time.sleep(1)
                continue
            elif choice == '0':
                console.print(Panel('[bold red]Keluar. Terima kasih.[bold red]'))
                return
            
            time.sleep(1)
        except KeyboardInterrupt:
            console.print('[red]Dibatalkan oleh user[/red]')
            return

def start_create_accounts():
    clear_screen()
    show_header_once()
    console.print('[bold green]Pembuatan akun sedang berjalan...[bold green]')
    
    if settings.get('use_file_email') and email_list_from_file:
        while email_list_from_file:
            email = get_email()
            if not email:
                break
            
            try:
                register_account()
                time.sleep(settings.get('delay', 3))
            except Exception as e:
                console.print(f'[red]Error saat register dengan email {email}: {e}[/red]')
        
        console.print('[bold green]Selesai menggunakan semua email dalam file![bold green]')
        return
    
    for _ in range(settings.get('limit', 1)):
        try:
            register_account()
            time.sleep(settings.get('delay', 3))
        except Exception as e:
            console.print(f'[red]Error saat register: {e}[/red]')

def set_limit():
    new_limit = IntPrompt.ask('Masukkan Limit (angka)', default=settings['limit'])
    settings['limit'] = max(1, min(9999, int(new_limit)))
    console.print(f'[green]Limit diperbarui menjadi {settings["limit"]}[green]')
    time.sleep(2)

def set_password():
    new_pw = Prompt.ask('Input Password (default)', default=settings['password'])
    settings['password'] = new_pw or 'FOUNDER'
    console.print('[green]Password diperbarui.[green]')
    time.sleep(2)

def toggle_temp_email():
    settings['use_temp_email'] = not settings['use_temp_email']
    
    if settings['use_temp_email']:
        settings['use_real_email'] = False
        settings['gmail_only'] = False
        settings['use_file_email'] = False
    
    console.print(f'[cyan]Temp Mail: {"AKTIF" if settings["use_temp_email"] else "OFF"}[cyan]')

def toggle_real_email():
    settings['use_real_email'] = not settings['use_real_email']
    
    if settings['use_real_email']:
        settings['use_temp_email'] = False
        settings['gmail_only'] = False
        settings['use_file_email'] = False
    
    console.print(f'[cyan]Real Email: {"AKTIF" if settings["use_real_email"] else "OFF"}[cyan]')

def toggle_gmail_only():
    settings['gmail_only'] = not settings['gmail_only']
    
    if settings['gmail_only']:
        settings['use_temp_email'] = False
        settings['use_real_email'] = False
        settings['use_file_email'] = False
    
    console.print(f'[cyan]Gmail Only: {"AKTIF" if settings["gmail_only"] else "OFF"}[cyan]')

def toggle_file_email():
    now = not settings.get('use_file_email', False)
    settings['use_file_email'] = now
    
    if not now:
        console.print('[yellow]Mode file email dimatikan.[/yellow]')
        return
    
    settings['gmail_only'] = False
    settings['use_temp_email'] = False
    settings['use_real_email'] = False
    
    if email_list_from_file:
        console.print(f'[green]File email sudah dimuat ({len(email_list_from_file)} email). Tidak memuat ulang.[/green]')
        return
    
    console.print('[cyan]Masukkan path file email:[/cyan]')
    path = input('File: ').strip()
    
    if not path:
        console.print('[yellow]Path kosong. Mode file email dibatalkan.[/yellow]')
        settings['use_file_email'] = False
        return
    
    if load_email_file(path):
        console.print('[green]Email file berhasil dimuat![/green]')
    else:
        settings['use_file_email'] = False

def check_saved_uid():
    if not SAVE_DIR.exists():
        console.print('[red]Folder result tidak ditemukan.[/red]')
        time.sleep(2)
        return
    
    uid_list = []
    
    for file in SAVE_DIR.glob('*.txt'):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if '|' not in line:
                        continue
                    
                    uid = line.split('|', 1)[0]
                    if uid.isdigit() and uid not in uid_list:
                        uid_list.append(uid)
        except:
            continue
    
    total_uid = len(uid_list)
    if total_uid == 0:
        console.print('[red]Belum ada UID tersimpan.[/red]')
        time.sleep(2)
        return
    
    console.print(Panel(f'Total UID di file: {total_uid}', title='CHECK UID (LIVE ONLY)', style='cyan'))
    
    tree = Tree('🟢 [bold green]UID LIVE DITEMUKAN[/bold green]')
    live_found = 0
    
    for index, uid in enumerate(uid_list, start=1):
        console.print(f'[grey50]({index}/{total_uid}) Mengecek UID → {uid}[/grey50]', end='\r')
        
        result = check_uid(uid)
        
        if result:
            live_found += 1
            name = result['name']
            
            tree.add(f'[green]{uid}[/green] → [bold white]{name}[/bold white]')
            console.print(f'[green]LIVE[/green] {uid} → {name}')
        
        time.sleep(random.uniform(*DELAY_RANGE))
    
    HEADER_CACHE['total_live'] = live_found
    
    console.print('\n')
    if live_found > 0:
        console.print(tree)
    else:
        console.print('[yellow]Tidak ada UID LIVE ditemukan.[/yellow]')
    
    console.print(Panel(f'Total LIVE: {live_found}', title='SELESAI', style='green'))
    input('Tekan Enter untuk kembali ke menu...')

if __name__ == '__main__':
    nickname = get_nickname()
    console.print(Panel(f'[bold green]Selamat datang, {nickname}![/bold green]', title='FACEBOOK ACCOUNT CREATOR'))
    time.sleep(2)
    
    try:
        while True:
            menu()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print('[red]Dibatalkan oleh user. Bye.[/red]')
        sys.exit(0)
    except Exception as e:
        console.print(f'[red]Terjadi kesalahan: {e}[/red]')
)
