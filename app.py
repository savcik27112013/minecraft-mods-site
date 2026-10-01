import json
import urllib.request
import urllib.parse
import ssl
from flask import Flask, request, Response

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

DATA = {
    "mods": [
        ("Ядро", [
            ("Fabric Loader", "Загрузчик Fabric — ставится первым", ""),
            ("Fabric API", "Библиотека, нужна почти всем модам", "fabric-api"),
            ("Mod Menu", "Список и настройки модов в игре", "modmenu"),
            ("Cloth Config API", "Окна настроек для модов", "cloth-config"),
            ("YACL", "Ещё одна библиотека конфигов", "yacl"),
        ]),
        ("Оптимизация", [
            ("Sodium", "Главный ускоритель графики", "sodium"),
            ("Lithium", "Ускоряет игровую логику и тики", "lithium"),
            ("Iris Shaders", "Шейдеры поверх Sodium", "iris"),
            ("Indium", "Совместимость Sodium с рендером модов", "indium"),
            ("Sodium Extra", "Доп. настройки графики для Sodium", "sodium-extra"),
            ("Reese's Sodium Options", "Удобное меню настроек Sodium", "reeses-sodium-options"),
            ("Starlight", "Переписанный движок света", "starlight"),
            ("FerriteCore", "Меньше памяти на блоки", "ferrite-core"),
            ("ModernFix", "Чинит лаги, ускоряет загрузку", "modernfix"),
            ("ImmediatelyFast", "Ускорение отрисовки", "immediatelyfast"),
            ("Entity Culling", "Не рисует сущности за стеной", "entityculling"),
            ("MoreCulling", "Отсечение невидимых граней", "moreculling"),
            ("Cull Less Leaves", "Скрывает листья внутри кроны", "cull-less-leaves"),
            ("Clumps", "Сливает шарики опыта", "clumps"),
            ("Krypton", "Ускоряет сеть", "krypton"),
            ("Memory Leak Fix", "Чинит утечки памяти", "memoryleakfix"),
            ("BadOptimizations", "Точечные оптимизации", "badoptimizations"),
            ("Dynamic FPS", "Режет FPS в фоне", "dynamic-fps"),
            ("Fastload", "Быстрая загрузка мира", "fastload"),
            ("Ksyxis", "Ускоряет вход в мир", "ksyxis"),
            ("LazyDFU", "Ускоряет старт игры", "lazydfu"),
            ("Smooth Boot", "Плавная загрузка без фризов", "smoothboot-fabric"),
            ("ThreadTweak", "Переносит нагрузку на потоки", "threadtweak"),
            ("Very Many Players", "Оптимизация сервера/мультиплеера", "vmp"),
            ("Noisium", "Быстрая генерация чанков", "noisium"),
            ("C2ME", "Параллельная генерация мира", "c2me-fabric"),
            ("Chunky", "Предзагрузка чанков", "chunky"),
            ("Bobby", "Держит дальние чанки в памяти", "bobby"),
            ("Distant Horizons", "Дальняя прорисовка (LOD)", "distanthorizons"),
            ("Exordium", "Медленнее рендерит HUD — больше FPS", "exordium"),
            ("Nvidium", "GPU-ускорение чанков (только NVIDIA)", "nvidium"),
            ("Debugify", "Чинит известные баги игры", "debugify"),
            ("VulkanMod", "Рендер на Vulkan API", "vulkanmod"),
            ("Raknetify", "Ускоряет мультиплеер", "raknetify"),
        ]),
        ("Графика и свет", [
            ("Continuity", "Соединённые текстуры", "continuity"),
            ("LambDynamicLights", "Живой свет от факелов и лавы", "lambdynamiclights"),
            ("Enhanced Block Entities", "Ускоряет сундуки и таблички", "ebe"),
            ("Falling Leaves", "Падающие листья с деревьев", "fallingleaves"),
            ("LambdaBetterGrass", "Красивая трава", "lambdabettergrass"),
            ("Polytone", "Единый рендер цветов и текстур", "polytone"),
            ("CIT Resewn", "Свои текстуры предметов", "cit-resewn"),
            ("Animatica", "Анимированные текстуры", "animatica"),
            ("Colormatic", "Свои цвета блоков", "colormatic"),
            ("Blur", "Размытие фона за меню", "blur-fabric"),
        ]),
        ("Анимации и модели", [
            ("Fancy World Animations", "Плавные анимации дверей, люков и блоков", "fwa"),
            ("Not Enough Animations", "Анимации рук, лука, карты", "not-enough-animations"),
            ("Eating Animation", "Анимация еды", "eating-animation"),
            ("First-person Model", "Видно тело от первого лица", "first-person-model"),
            ("3D Skin Layers", "Объёмные слои скина", "3dskinlayers"),
            ("Entity Model Features", "EMF — кастомные модели мобов", "entity-model-features"),
            ("Entity Texture Features", "ETF — случайные текстуры мобов", "entitytexturefeatures"),
            ("Wavey Capes", "Физика плащей", "wavey-capes"),
            ("Capes", "Плащи с разных сервисов", "capes"),
            ("Do a Barrel Roll", "Управление элитрами", "do-a-barrel-roll"),
            ("Shoulder Surfing", "Камера от третьего лица", "shoulder-surfing-reloaded"),
            ("Custom Skin Loader", "Скины с любого сервера", "custom-skin-loader"),
            ("Figura", "Полностью кастомные аватары с анимацией", "figura"),
            ("Better Third Person", "Улучшенный вид от третьего лица", "better-third-person"),
            ("Player Animator", "Анимации игрока из ресурспаков", "playeranimator"),
            ("Animation Overhaul", "Новые анимации бега и движений", "animation-overhaul"),
            ("FancyMenu", "Кастомные меню и анимации интерфейса", "fancymenu"),
            ("Skin Shuffle", "Меняешь скин на лету в игре", "skinshuffle"),
            ("Show Me Your Skin", "Видит скины и плащи других", "show-me-your-skin"),
        ]),
        ("Карты", [
            ("VoxelMap", "Миникарта и карта мира", "voxelmap"),
            ("Xaero's Minimap", "Лёгкая миникарта", "xaeros-minimap"),
            ("Xaero's World Map", "Полноэкранная карта мира", "xaeros-world-map"),
            ("JourneyMap", "Карта в реальном времени", "journeymap"),
        ]),
        ("Интерфейс и QoL", [
            ("Roughly Enough Items", "REI — просмотр рецептов", "rei"),
            ("JEI", "Классический просмотр рецептов", "jei"),
            ("EMI", "Лёгкий просмотр рецептов", "emi"),
            ("AppleSkin", "Показывает сытость еды", "appleskin"),
            ("BetterF3", "Улучшенный F3-экран", "betterf3"),
            ("Controlling", "Удобный поиск по клавишам", "controlling"),
            ("Mouse Tweaks", "Быстрый перенос предметов мышью", "mouse-tweaks"),
            ("Inventory Move", "Двигаешься с открытым инвентарём", "invmove"),
            ("Zoomify", "Плавный зум", "zoomify"),
            ("Inventory Profiles Next", "Сортировка инвентаря", "inventory-profiles-next"),
            ("Inventory HUD+", "Инвентарь поверх экрана", "inventory-hud"),
            ("Chat Heads", "Головы игроков в чате", "chat-heads"),
            ("No Chat Reports", "Убирает репорты в чате", "no-chat-reports"),
            ("Boat Item View", "Предмет в руке в лодке", "boat-item-view"),
            ("Better Mount HUD", "Полоски здоровья лошади", "better-mount-hud"),
            ("Jade", "Показывает, на какой блок смотришь", "jade"),
            ("WTHIT", "Аналог Jade — инфо о блоке", "wthit"),
            ("Enchantment Descriptions", "Описание зачарований", "enchantment-descriptions"),
            ("Better Advancements", "Красивые достижения", "better-advancements"),
            ("Traveler's Titles", "Названия биомов на экране", "travelers-titles"),
            ("Trinkets", "Слоты для колец и амулетов", "trinkets"),
        ]),
        ("Приколы и развлечения", [
            ("Emotecraft", "Танцы и эмоции игрока", "emotecraft"),
            ("Joy of Painting", "Рисуй картины прямо в игре", "joy-of-painting"),
            ("Simple Voice Chat", "Голосовой чат в игре", "simple-voice-chat"),
            ("Freecam", "Свободная камера", "freecam"),
            ("Camera Utils", "Плавная камера и зум", "camera-utils"),
            ("Carry On", "Переноси блоки и мобов руками", "carry-on"),
            ("Wall-Jump", "Бег по стенам", "wall-jump"),
            ("Swing Through Grass", "Удар сквозь траву", "swingthroughgrass"),
            ("Passable Foliage", "Проходи сквозь листья", "passable-foliage"),
            ("Corpse", "Труп с вещами после смерти", "corpse"),
            ("Player Graves", "Могила с инвентарём", "player-graves"),
            ("Detail Armor Bar", "Полоска прочности брони", "detail-armor-bar"),
            ("Subtle Effects", "Красивые частицы", "subtle-effects"),
            ("Not Enough Crashes", "Читаемый отчёт о краше", "notenoughcrashes"),
        ]),
        ("Мир и генерация", [
            ("Terralith", "120+ новых биомов", "terralith"),
            ("BetterNether", "Переработанный Нижний мир", "betternether"),
            ("BetterEnd", "Переработанный Энд", "betterend"),
            ("Biomes O' Plenty", "Множество биомов и деревьев", "biomes-o-plenty"),
            ("Oh The Biomes We've Gone", "Десятки новых биомов и деревьев", "oh-the-biomes-weve-gone"),
            ("The Twilight Forest", "Новое измерение — Сумеречный лес", "the-twilight-forest"),
        ]),
        ("Мир и структуры", [
            ("YUNG's Better Dungeons", "Улучшенные подземелья", "yungs-better-dungeons"),
            ("YUNG's Better Mineshafts", "Улучшенные шахты", "yungs-better-mineshafts"),
            ("YUNG's Better Strongholds", "Улучшенные крепости", "yungs-better-strongholds"),
            ("YUNG's Better Desert Temples", "Улучшенные пустынные храмы", "yungs-better-desert-temples"),
            ("YUNG's Better Ocean Monuments", "Улучшенные океанские монументы", "yungs-better-ocean-monuments"),
            ("Structory", "Новые руины и постройки", "structory"),
            ("Towns and Towers", "Города и башни в мире", "towns-and-towers"),
            ("When Dungeons Arise", "Большие данжи и замки", "when-dungeons-arise"),
            ("Repurposed Structures", "Структуры ванили в новых местах", "repurposed-structures"),
            ("Explorify", "Новые точки интереса для карт", "explorify"),
        ]),
        ("Контент и мобы", [
            ("Create", "Механика шестерёнок и конвейеров", "create"),
            ("Farmer's Delight", "Кулинария и фермерство", "farmers-delight"),
            ("Ad Astra", "Космос и ракеты", "ad-astra"),
            ("Waystones", "Телепорты между точками", "waystones"),
            ("Traveler's Backpack", "Рюкзаки", "travelersbackpack"),
            ("Iron Chests", "Улучшенные сундуки", "iron-chests"),
            ("Sophisticated Backpacks", "Прокачиваемые рюкзаки", "sophisticated-backpacks"),
            ("Applied Energistics 2", "AE2 — хранение предметов", "ae2"),
            ("You're in Grave Danger", "Могила с вещами после смерти", "yigd"),
            ("Better Combat", "Комбо и новые атаки", "better-combat"),
            ("Naturalist", "Живые животные", "naturalist"),
            ("Friends & Foes", "Неиспользованные мобы Mojang", "friends-and-foes"),
            ("Alex's Mobs", "89 новых существ", "alexs-mobs"),
            ("Supplementaries", "Множество декора и механик", "supplementaries"),
            ("Amendments", "Дополнение к Supplementaries", "amendments"),
            ("Origins", "Выбираешь расу со способностями", "origins"),
            ("Pehkui", "Меняет размер существ", "pehkui"),
            ("Carpet", "Инструменты для серверов", "carpet"),
        ]),
        ("Звук и эффекты", [
            ("Presence Footsteps", "Реалистичные шаги", "presence-footsteps"),
            ("Sound Physics Remastered", "Эхо и объёмный звук", "sound-physics-remastered"),
            ("AmbientSounds", "Звуки окружения", "ambientsounds"),
            ("Effective", "Каскады воды и брызги", "effective"),
            ("Particular", "Частицы падения и пыль", "particular"),
            ("Visuality", "Искры, кристаллы, слаймы", "visuality"),
        ]),
    ],
    "resourcepacks": [
        ("Ресурспаки", [
            ("Fresh Animations", "Анимации мобов и игрока", "fresh-animations"),
            ("Default Dark Mode", "Тёмный интерфейс", "default-dark-mode"),
            ("Stay True", "Чистые текстуры 32x", "stay-true"),
            ("Bare Bones", "Пластилиновый мультяшный стиль", "bare-bones"),
            ("Mizuno's 16 Craft", "Уютные детализированные текстуры", "mizunos-16-craft"),
            ("CreatorPack", "Реалистичные текстуры", "creator-pack"),
            ("Better Dogs", "Много пород собак", "better-dogs"),
            ("Classic 3D", "Объёмные блоки и предметы", "classic-3d"),
            ("Better Leaves", "Красивая листва", "better-leaves"),
            ("Visual Enchantments", "Свои иконки зачарований", "visual-enchantments"),
            ("Crops 3D", "Объёмные посевы", "crops-3d"),
            ("Dandelion", "Светлые чистые текстуры", "dandelion"),
            ("Dramatic Skys", "Реалистичное небо", "dramatic-skys"),
            ("New Default+", "Обновлённая ваниль", "newdefaultplus"),
            ("Better Vanilla Building", "Текстуры для строителей", "better-vanilla-building"),
            ("Faithful 32x", "Классика в 32x", ""),
            ("Sphax PureBDcraft", "Мультяшный стиль BDcraft", ""),
            ("Vanilla Tweaks", "Конструктор мелких улучшений", ""),
        ]),
    ],
    "shaders": [
        ("Шейдеры", [
            ("Complementary Reimagined", "Самый популярный, красиво и легко", "complementary-reimagined"),
            ("Complementary Unbound", "Требовательная версия Complementary", "complementary-unbound"),
            ("BSL Shaders", "Мягкий свет и объёмный туман", "bsl-shaders"),
            ("MakeUp Ultra Fast", "Максимум FPS среди шейдеров", "makeup-ultra-fast-shaders"),
            ("Solas Shader", "Свежий шейдер с тёплой картинкой", "solas-shader"),
            ("Rethinking Voxels", "Воксельный свет, реалистично", "rethinking-voxels"),
            ("Photon Shader", "Современная освещённость", "photon-shader"),
            ("Bliss Shader", "Фотореализм с мягким светом", "bliss-shader"),
            ("Soft Voxels", "Красивый воксельный GI", "soft-voxels"),
            ("Pastel Shaders", "Пастельные мягкие цвета", "pastel-shaders"),
            ("Nostalgia", "Тёплая ностальгическая картинка", "nostalgia"),
            ("Super Duper Vanilla", "Ванильный стиль с красивым светом", "super-duper-vanilla"),
            ("AstraLex", "Много эффектов на базе BSL", "astralex"),
            ("Chocapic13", "Классические шейдеры", "chocapic13-shaders"),
            ("Sildur's Shaders", "Классика, лёгкие версии", ""),
            ("SEUS", "PTGI — трассировка пути", ""),
        ]),
    ],
}

TABS = [("mods", "Моды"), ("resourcepacks", "Ресурспаки"), ("shaders", "Шейдеры")]
VERSIONS = ["1.21", "1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10", "1.21.11"]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def render():
    tabs_html = []
    for key, label in TABS:
        active = " active" if key == "mods" else ""
        tabs_html.append(f'<button class="tab{active}" data-tab="{key}">{label}</button>')
    contents = []
    for key, label in TABS:
        hidden = "" if key == "mods" else ' style="display:none"'
        sections = []
        for ci, (cat, items) in enumerate(DATA[key]):
            cards = []
            for ni, (name, desc, slug) in enumerate(items):
                search = f"{name} {desc}".lower()
                cards.append(
                    f'<div class="card" style="animation-delay:{ni*0.015}s" data-search="{esc(search)}" '
                    f'data-name="{esc(name)}" data-desc="{esc(desc)}" data-slug="{esc(slug)}" '
                    f'data-kind="{key}" onclick="openModal(this)">'
                    f'<div class="name">{esc(name)}</div>'
                    f'<div class="desc">{esc(desc)}</div>'
                    f'<span class="more">Подробнее</span>'
                    "</div>"
                )
            sections.append(
                f'<div class="cat-head"><h2>{esc(cat)}</h2><span class="count">{len(items)}</span></div>'
                f'<div class="grid">{"".join(cards)}</div>'
            )
        contents.append(f'<div class="tab-content" data-content="{key}"{hidden}>{"".join(sections)}</div>')
    versions = "".join(
        f'<option value="{v}"{" selected" if v == "1.21.11" else ""}>{v}</option>' for v in VERSIONS
    )
    return "".join(tabs_html), "".join(contents), versions

tabs_html, contents, versions = render()

HTML = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Minecraft Fabric — каталог модов, ресурспаков и шейдеров</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; color: #e6edf3; font-family: Segoe UI, system-ui, sans-serif; background: linear-gradient(130deg, #0d1117, #14243a, #251430, #0d1117); background-size: 400% 400%; animation: bgshift 22s ease infinite; background-attachment: fixed; }}
  @keyframes bgshift {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
  header {{ padding: 20px 20px 14px; }}
  .top {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ margin: 0 0 6px; font-size: 24px; }}
  .sub {{ color: #8b949e; margin: 0 0 14px; font-size: 14px; }}
  .controls {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
  #search {{ flex: 1; min-width: 200px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; padding: 10px 14px; font-size: 15px; outline: none; }}
  #search:focus {{ border-color: #58a6ff; }}
  select {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; padding: 10px 12px; font-size: 14px; outline: none; }}
  .tabs {{ max-width: 1100px; margin: 16px auto 0; display: flex; gap: 8px; flex-wrap: wrap; }}
  .tab {{ background: #161b22; border: 1px solid #30363d; border-radius: 999px; color: #c9d1d9; padding: 8px 16px; font-size: 14px; cursor: pointer; }}
  .tab.active {{ background: #1f6feb; border-color: #1f6feb; color: #fff; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 8px 20px 80px; }}
  .cat-head {{ display: flex; align-items: center; gap: 10px; margin: 32px 0 14px; }}
  h2 {{ font-size: 20px; color: #58a6ff; margin: 0; }}
  .count {{ background: #1f2428; color: #8b949e; border-radius: 999px; padding: 2px 10px; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 12px; }}
  .card {{ background: rgba(22,27,34,.85); border: 1px solid #30363d; border-radius: 12px; padding: 15px; display: flex; flex-direction: column; gap: 9px; cursor: pointer; transition: transform .18s, border-color .18s, box-shadow .18s; animation: fadeIn .5s ease backwards; }}
  @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .card:hover {{ transform: translateY(-4px); border-color: #58a6ff; box-shadow: 0 8px 24px rgba(88,166,255,.15); }}
  .name {{ font-weight: 600; font-size: 16px; }}
  .desc {{ color: #8b949e; font-size: 13px; flex: 1; }}
  .more {{ color: #58a6ff; font-size: 13px; }}
  #modal {{ position: fixed; inset: 0; background: rgba(0,0,0,.7); display: none; align-items: center; justify-content: center; z-index: 50; padding: 20px; }}
  #modal.show {{ display: flex; }}
  .modal-box {{ background: #161b22; border: 1px solid #30363d; border-radius: 14px; max-width: 480px; width: 100%; padding: 24px; }}
  .modal-box h3 {{ margin: 0 0 10px; font-size: 22px; color: #58a6ff; }}
  .modal-box p {{ color: #c9d1d9; line-height: 1.5; margin: 0 0 20px; }}
  .modal-actions {{ display: flex; gap: 10px; }}
  .modal-actions a, .modal-actions button {{ flex: 1; text-align: center; border-radius: 8px; padding: 11px; font-size: 15px; font-weight: 600; cursor: pointer; text-decoration: none; border: none; color: #fff; }}
  .dl {{ background: linear-gradient(135deg, #238636, #1f6feb); display: none; }}
  .close {{ background: #30363d; }}
  @media (max-width: 520px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <div class="top">
    <h1>Minecraft Fabric — каталог модов, ресурспаков и шейдеров</h1>
    <p class="sub">Версия: <b id="ver-label">1.21.11</b> · скачивание идёт через этот сайт, Modrinth не открывается</p>
    <div class="controls">
      <input id="search" type="text" placeholder="Поиск: sodium, шейдер, анимация...">
      <select id="ver">{versions}</select>
    </div>
  </div>
  <div class="tabs">{tabs_html}</div>
</header>
<main>{contents}</main>
<div id="modal">
  <div class="modal-box">
    <h3 id="m-title"></h3>
    <p id="m-desc"></p>
    <div class="modal-actions">
      <a id="m-dl" class="dl" target="_blank" rel="noopener">Скачать</a>
      <button class="close" onclick="closeModal()">Закрыть</button>
    </div>
  </div>
</div>
<script>
  const verSel = document.getElementById('ver');
  const verLabel = document.getElementById('ver-label');
  verSel.addEventListener('change', () => {{ verLabel.textContent = verSel.value; }});
  document.querySelectorAll('.tab').forEach(t => {{
    t.addEventListener('click', () => {{
      document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      const key = t.dataset.tab;
      document.querySelectorAll('.tab-content').forEach(c => {{
        c.style.display = c.dataset.content === key ? '' : 'none';
      }});
    }});
  }});
  function openModal(el) {{
    document.getElementById('m-title').textContent = el.dataset.name;
    document.getElementById('m-desc').textContent = el.dataset.desc;
    const dl = document.getElementById('m-dl');
    if (el.dataset.slug) {{
      dl.style.display = 'block';
      dl.href = '/download?slug=' + encodeURIComponent(el.dataset.slug) + '&kind=' + el.dataset.kind + '&version=' + verSel.value;
    }} else {{
      dl.style.display = 'none';
    }}
    document.getElementById('modal').classList.add('show');
  }}
  function closeModal() {{ document.getElementById('modal').classList.remove('show'); }}
  document.getElementById('modal').addEventListener('click', (e) => {{ if (e.target.id === 'modal') closeModal(); }});
  const q = document.getElementById('search');
  q.addEventListener('input', () => {{
    const v = q.value.toLowerCase();
    document.querySelectorAll('.card').forEach(c => {{ c.style.display = c.dataset.search.includes(v) ? '' : 'none'; }});
  }});
</script>
</body>
</html>"""

def find_file(slug, kind, version):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"game_versions": '["' + version + '"]'}
    loader = {"mods": "fabric", "shaders": "iris"}.get(kind)
    if loader:
        params["loaders"] = '["' + loader + '"]'
    url = "https://api.modrinth.com/v2/project/" + slug + "/version?" + urllib.parse.urlencode(params)
    data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30).read().decode())
    if not data and loader:
        params.pop("loaders", None)
        url = "https://api.modrinth.com/v2/project/" + slug + "/version?" + urllib.parse.urlencode(params)
        data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30).read().decode())
    for v in data:
        files = v.get("files") or []
        if files:
            return files[0]["url"], files[0]["filename"]
    return None

@app.route("/")
def index():
    return HTML

@app.route("/download")
def download():
    slug = request.args.get("slug", "")
    kind = request.args.get("kind", "mods")
    version = request.args.get("version", "1.21.11")
    info = find_file(slug, kind, version)
    if not info:
        return "не найдено", 404
    file_url, filename = info
    req = urllib.request.Request(file_url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=120).read()
    return Response(data, mimetype="application/octet-stream",
                    headers={"Content-Disposition": 'attachment; filename="' + filename + '"'})
