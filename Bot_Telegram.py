from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAZIONE ---
import os
# Legge il token e l'username dalle variabili d'ambiente del server
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TUO_USERNAME = os.environ.get("@simomall")
# --- UTILITY: CREAZIONE LINK DI CONTATTO ---

def create_contact_link(product_name):
    """Crea il link t.me con messaggio preimpostato."""
    base_message = f"Ciao @{TUO_USERNAME}, vorrei acquistare: {product_name}."
    # Sostituisce lo spazio con %20 per l'URL encoding
    link = f"https://t.me/{TUO_USERNAME}?text={base_message.replace(' ', '%20')}"
    return link

# --- 1. FUNZIONI MENU LIVELLO 1 (/start) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Invia il messaggio di benvenuto con i pulsanti del menu principale."""
    keyboard = [
        [InlineKeyboardButton("Linux USB", callback_data='menu_linux')],
        [InlineKeyboardButton("Windows", callback_data='menu_windows')],
        [InlineKeyboardButton("RetroGaming", callback_data='menu_retrogaming')],
        [InlineKeyboardButton("MacOS", callback_data='menu_macos')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Se il comando arriva da /start o da un callback
    if update.message:
        await update.message.reply_text('Benvenuto! Scegli una categoria:', reply_markup=reply_markup)
    else: # Usato per il ritorno da un sottomenu
        query = update.callback_query
        await query.answer()
        await query.edit_message_text('Scegli una categoria:', reply_markup=reply_markup)

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il ritorno al menu principale da un callback."""
    await start(update, context)


# --- 2. FUNZIONI MENU LIVELLO 2 (Sotto-categorie) ---

async def linux_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu Linux: Multi Boot o Single Boot."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Multi Boot", callback_data='menu_multi_boot')],
        [InlineKeyboardButton("Single Boot", callback_data='menu_single_boot')],
        # NUOVO TASTO INDIETRO
        [InlineKeyboardButton("🔙 Torna al Menu Principale", callback_data='menu_start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Hai scelto Linux. Scegli il tipo di configurazione:", reply_markup=reply_markup)

async def windows_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu Windows: Opzioni specifiche."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Windows 10", callback_data='prodotto_win10')],
        [InlineKeyboardButton("Windows 11", callback_data='prodotto_win11')],
        [InlineKeyboardButton("Office", callback_data='prodotto_office')],
        [InlineKeyboardButton("Contattaci e scegli tu!", url=create_contact_link("Richiesta Windows Personalizzata"))],
        # NUOVO TASTO INDIETRO
        [InlineKeyboardButton("🔙 Torna al Menu Principale", callback_data='menu_start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Hai scelto Windows. Seleziona un'opzione:", reply_markup=reply_markup)

async def retrogaming_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu Retrogaming: Opzioni aggiunte."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Amiga500", callback_data='prodotto_amiga500'),
            InlineKeyboardButton("Commodore64", callback_data='prodotto_c64'),
        ],
        [
            InlineKeyboardButton("ZX Spectrum", callback_data='prodotto_spectrum'),
            InlineKeyboardButton("Mega Sega Drive", callback_data='prodotto_megadrive'),
        ],
        # NUOVO TASTO INDIETRO
        [InlineKeyboardButton("🔙 Torna al Menu Principale", callback_data='menu_start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Ottima scelta! Seleziona una console:", reply_markup=reply_markup)

async def macos_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu MacOS: Reindirizzamento diretto."""
    query = update.callback_query
    await query.answer()
    
    # Crea link per reindirizzamento diretto con messaggio specifico
    link_contatto = create_contact_link("Versione MacOS Desiderata")
    
    keyboard = [
        [InlineKeyboardButton("Comunicaci la versione desiderata!", url=link_contatto)],
        # NUOVO TASTO INDIETRO
        [InlineKeyboardButton("🔙 Torna al Menu Principale", callback_data='menu_start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Hai scelto MacOS. Clicca qui per comunicare direttamente la versione:", reply_markup=reply_markup)

# --- 3. FUNZIONI MENU LIVELLO 3 (Single Boot e Multi Boot) ---

async def single_boot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista delle opzioni Single Boot."""
    query = update.callback_query
    await query.answer()

    # Opzioni per Single Boot
    os_list = ["ZorinOS", "Linux Mint", "Ubuntu", "Kali", "Tails", "Lubuntu", "Fedora", "CachyOS", "Pop!_OS", "ElementaryOS"]
    
    keyboard = []
    for os_name in os_list:
        # Crea un callback data unico per ogni OS (es. 'os_zorinos')
        callback_data = 'os_' + os_name.replace('!', '').replace('-', '').replace(' ', '').lower()
        keyboard.append([InlineKeyboardButton(os_name, callback_data=callback_data)])
        
    # NUOVO TASTO INDIETRO: Torna al menu Linux (Livello 2)
    keyboard.append([InlineKeyboardButton("🔙 Torna al Menu Linux", callback_data='menu_linux')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Seleziona il tuo sistema operativo Single Boot:", reply_markup=reply_markup)

async def multi_boot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista delle opzioni Multi Boot."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Privacy (Kali e Tails)", callback_data='prodotto_multiboot_privacy')],
        [InlineKeyboardButton("Starter (ZorinOS, Mint, Lubuntu)", callback_data='prodotto_multiboot_starter')],
        [InlineKeyboardButton("Personalizza con i tuoi OS preferiti!", url=create_contact_link("Multi Boot Personalizzato"))],
        # NUOVO TASTO INDIETRO: Torna al menu Linux (Livello 2)
        [InlineKeyboardButton("🔙 Torna al Menu Linux", callback_data='menu_linux')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Seleziona il tuo pacchetto Multi Boot:", reply_markup=reply_markup)


# --- 4. FUNZIONI SCHEDA PRODOTTO (Gestione generica del prodotto) ---

async def show_product_card(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str, product_name: str, description: str, back_callback: str) -> None:
    """
    Genera la scheda prodotto finale con link di contatto.
    Aggiunge il tasto "Torna Indietro" usando back_callback.
    """
    query = update.callback_query
    await query.answer()

    link_contatto = create_contact_link(product_name)
    
    keyboard = [
        [InlineKeyboardButton(f"Contatta @{TUO_USERNAME} per Acquistare!", url=link_contatto)],
        # NUOVO TASTO INDIETRO: Usa il callback fornito dalla funzione chiamante
        [InlineKeyboardButton("🔙 Torna Indietro", callback_data=back_callback)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"✨ **{product_name}** ✨\n\n{description}"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# --- 5. MAPPATURA DEI PRODOTTI/OS (Livello 4) ---

async def handle_os_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    os_key = query.data.replace('os_', '') # Rimuove il prefisso 'os_'
    
    os_display_name = {
        'zorinos': 'ZorinOS', 'linuxmint': 'Linux Mint', 'ubuntu': 'Ubuntu', 
        'kali': 'Kali', 'tails': 'Tails', 'lubuntu': 'Lubuntu', 
        'fedora': 'Fedora', 'cachyos': 'CachyOS', 'popos': 'Pop!_OS', 
        'elementaryos': 'ElementaryOS'
    }.get(os_key, os_key.capitalize())
    
    description = f"Hai selezionato *{os_display_name}*. Riceverai una chiavetta USB con il sistema operativo pronto all'installazione."
    
    # CALLBACK DI RITORNO: Deve tornare al menu Single Boot
    await show_product_card(update, context, os_key, os_display_name, description, 'menu_single_boot')


async def handle_product_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    product_key = query.data

    products = {
        # RETROGAMIN
        'prodotto_amiga500': ("Amiga500 Pack", "Contiene un Amiga500 preconfigurato con una selezione di classici.", 'menu_retrogaming'),
        'prodotto_c64': ("Commodore64 Pack", "La leggenda dei bit, pronto all'uso con i giochi più iconici.", 'menu_retrogaming'),
        'prodotto_spectrum': ("ZX Spectrum Pack", "L'esperienza 8-bit britannica, con i giochi caricabili da nastro.", 'menu_retrogaming'),
        'prodotto_megadrive': ("Mega Sega Drive Pack", "L'intera libreria SEGA 16-bit su un unico supporto.", 'menu_retrogaming'),
        
        # WINDOWS
        'prodotto_win10': ("Windows 10 USB", "Installazione pulita e aggiornata di Windows 10 su USB.", 'menu_windows'),
        'prodotto_win11': ("Windows 11 USB", "Installazione pulita e aggiornata di Windows 11 su USB.", 'menu_windows'),
        'prodotto_office': ("Pacchetto Office", "La suite Microsoft Office preinstallata.", 'menu_windows'),
        
        # MULTI BOOT
        'prodotto_multiboot_privacy': ("Multi Boot: Privacy (Kali e Tails)", "Ideale per l'anonimato e la sicurezza informatica.", 'menu_multi_boot'),
        'prodotto_multiboot_starter': ("Multi Boot: Starter (ZorinOS, Mint, Lubuntu)", "Perfetto per chi si avvicina al mondo Linux.", 'menu_multi_boot'),
    }

    # Estrai i dati del prodotto e il callback di ritorno
    product_data = products.get(product_key, ("Prodotto non Trovato", "Descrizione non disponibile.", 'menu_start'))
    product_name, description, back_callback = product_data
    
    await show_product_card(update, context, product_key, product_name, description, back_callback)


# --- 6. GESTORE DEI CALLBACK E MAIN FUNCTION ---

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce tutte le azioni dei pulsanti inline e indirizza alla funzione corretta."""
    query = update.callback_query
    data = query.data
    
    # 1. LIVELLO 1 (Menu Principale)
    if data == 'menu_linux':
        await linux_menu(update, context)
    elif data == 'menu_windows':
        await windows_menu(update, context)
    elif data == 'menu_retrogaming':
        await retrogaming_menu(update, context)
    elif data == 'menu_macos':
        await macos_menu(update, context)
    elif data == 'menu_start':
        await start_callback(update, context)

    # 2. LIVELLO 2 (Sotto-menu Linux)
    elif data == 'menu_single_boot':
        await single_boot_menu(update, context)
    elif data == 'menu_multi_boot':
        await multi_boot_menu(update, context)

    # 3. LIVELLO 3 e 4 (Schede Prodotto: Multi Boot, Retrogaming, Windows)
    elif data.startswith('prodotto_'):
        await handle_product_selection(update, context)
    
    # 4. LIVELLO 4 (Selezione Single Boot OS)
    elif data.startswith('os_'):
        await handle_os_selection(update, context)
        
    await query.answer() # Chiude il loading del pulsante in Telegram


def main() -> None:
    """Avvia il bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Gestori per i comandi classici
    application.add_handler(CommandHandler("start", start))
    
    # Gestore per i pulsanti inline (CallbackQuery)
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Avvia l'ascolto dei messaggi
    print("Bot avviato e in ascolto...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()