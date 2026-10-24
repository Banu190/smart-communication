import { useState, type ReactNode } from "react";

type IconName =
  | "home" | "users" | "cards" | "sparkles" | "folder" | "chart"
  | "settings" | "bell" | "chevron" | "arrow" | "message" | "calendar"
  | "shield" | "plus" | "logout" | "chat";

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, ReactNode> = {
    home: <><path d="m3 10 9-7 9 7" /><path d="M5 9v11h14V9M9 20v-6h6v6" /></>,
    users: <><path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="10" cy="7" r="4" /><path d="M20 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></>,
    cards: <><rect x="3" y="4" width="18" height="16" rx="3" /><path d="m8 13 3-3 3 3 2-2 3 3M8 8h.01" /></>,
    sparkles: <><path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2L12 3Z" /><path d="m19 14 1 2.5 2.5 1-2.5 1L19 21l-1-2.5-2.5-1 2.5-1L19 14ZM5 2l.8 2.2L8 5l-2.2.8L5 8l-.8-2.2L2 5l2.2-.8L5 2Z" /></>,
    folder: <><path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" /></>,
    chart: <><path d="M3 3v18h18" /><path d="m19 9-5 5-4-4-5 5" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="m19.4 15 .1.1a1.7 1.7 0 0 1-2.4 2.4l-.1-.1a1.7 1.7 0 0 0-2.9 1.2v.2a1.7 1.7 0 0 1-3.4 0v-.2a1.7 1.7 0 0 0-2.9-1.2l-.1.1a1.7 1.7 0 0 1-2.4-2.4l.1-.1a1.7 1.7 0 0 0-1.2-2.9H4a1.7 1.7 0 0 1 0-3.4h.2a1.7 1.7 0 0 0 1.2-2.9l-.1-.1a1.7 1.7 0 0 1 2.4-2.4l.1.1a1.7 1.7 0 0 0 2.9-1.2V4a1.7 1.7 0 0 1 3.4 0v.2a1.7 1.7 0 0 0 2.9 1.2l.1-.1a1.7 1.7 0 0 1 2.4 2.4l-.1.1a1.7 1.7 0 0 0 1.2 2.9h.2a1.7 1.7 0 0 1 0 3.4h-.2a1.7 1.7 0 0 0-1.2.9Z" /></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 21h4" /></>,
    chevron: <path d="m9 18 6-6-6-6" />,
    arrow: <><path d="M5 12h14" /><path d="m13 6 6 6-6 6" /></>,
    message: <><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z" /></>,
    calendar: <><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M16 3v4M8 3v4M3 11h18" /><path d="m9 16 2 2 4-4" /></>,
    shield: <><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z" /><path d="m9 12 2 2 4-4" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    logout: <><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><path d="m16 17 5-5-5-5M21 12H9" /></>,
    chat: <><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.5 8.5 0 0 1 12.5 3h.5a8.5 8.5 0 0 1 8 8v.5Z" /><path d="M8 12h.01M12 12h.01M16 12h.01" /></>,
  };

  return <svg aria-hidden="true" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

const navigation: { label: string; icon: IconName }[] = [
  { label: "Басты бет", icon: "home" },
  { label: "Балалар профилдері", icon: "users" },
  { label: "Карточкалар кітапханасы", icon: "cards" },
  { label: "ЖИ генераторы", icon: "sparkles" },
  { label: "Карточкалар жинағы", icon: "folder" },
  { label: "Статистика", icon: "chart" },
  { label: "Баптаулар", icon: "settings" },
];

const cards = [
  { name: "Су", emoji: "🥛", tone: "blue", category: "Күнделікті қажеттілік" },
  { name: "Алма", emoji: "🍎", tone: "peach", category: "Тамақ пен сусын" },
  { name: "Нан", emoji: "🍞", tone: "yellow", category: "Тамақ пен сусын" },
  { name: "Ана", emoji: "👩🏻", tone: "lilac", category: "Адамдар" },
  { name: "Дәретхана", emoji: "🚽", tone: "mint", category: "Күнделікті қажеттілік" },
  { name: "Ойнау", emoji: "⚽", tone: "blue", category: "Әрекеттер" },
];

const initialChildren = [
  { name: "Асылым", detail: "6 жаста · 32 карточка", initials: "А", color: "peach" },
  { name: "Мирас", detail: "4 жаста · 18 карточка", initials: "М", color: "peach" },
];

export default function Home() {
  const [activePage, setActivePage] = useState("Басты бет");
  const [selectedChild, setSelectedChild] = useState("Асылым");
  const [children, setChildren] = useState(initialChildren);
  const [notice, setNotice] = useState("");
  const [language, setLanguage] = useState("KZ");

  const announce = (message: string) => {
    setNotice(message);
    window.setTimeout(() => setNotice(""), 3200);
  };

  const addChild = () => {
    if (children.some((child) => child.name === "Жаңа бала")) {
      setSelectedChild("Жаңа бала");
      return;
    }
    setChildren((current) => [...current, {
      name: "Жаңа бала",
      detail: "Жаңа профиль",
      initials: "Ж",
      color: "peach",
    }]);
    setSelectedChild("Жаңа бала");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" onClick={() => setActivePage("Басты бет")}>
          <span className="brand-mark"><Icon name="message" size={20} /></span>
          <span className="brand-word">SÖYLE</span>
        </a>
        <p className="brand-caption">Ата-ана кабинеті</p>

        <nav className="main-nav" aria-label="Негізгі навигация">
          {navigation.map((item) => (
            <button
              key={item.label}
              className={`nav-item${activePage === item.label ? " active" : ""}`}
              onClick={() => {
                setActivePage(item.label);
                if (item.label !== "Басты бет") announce(`${item.label} бөлімі әзірленуде`);
              }}
            >
              <Icon name={item.icon} size={17} /><span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-tip">
          <span className="tip-icon"><Icon name="sparkles" size={16} /></span>
          <strong>Бірге үйренеміз</strong>
          <p>Әр сөз — үлкен қадам. Балаңыздың жетістігін бірге атап өтейік!</p>
          <button onClick={() => announce("Жаттығулар бөлімі әзірленуде")}>Жаттығулар <Icon name="arrow" size={13} /></button>
        </div>

        <div className="sidebar-bottom">
          <button className="account" onClick={() => announce("Аккаунт баптаулары әзірленуде")}>
            <span className="avatar avatar-small">А</span>
            <span><strong>Айгүл</strong><small>Ата-ана</small></span>
            <Icon name="chevron" size={15} />
          </button>
          <button className="logout" onClick={() => announce("Сіз жүйеден шыққан жоқсыз")}><Icon name="logout" size={16} /> Шығу</button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb"><span>Ата-ана кабинеті</span><span>/</span><strong>{activePage}</strong></div>
          <div className="top-actions">
            <span className="safe-mode"><Icon name="shield" size={15} /> Қорғалған режим</span>
            <button className="icon-button notification-button" aria-label="Хабарландырулар" onClick={() => announce("Жаңа хабарландыру жоқ")}><Icon name="bell" size={18} /><i /></button>
            <button className="language-button" onClick={() => setLanguage((current) => current === "KZ" ? "RU" : "KZ")}>{language} <span>⌄</span></button>
            <button className="avatar avatar-top" aria-label="Профиль" onClick={() => announce("Профиль баптаулары әзірленуде")}>А</button>
          </div>
        </header>

        <div className="page-content">
          <section className="welcome-row">
            <div>
              <p className="eyebrow">Қайта келгеніңізге қуаныштымыз</p>
              <h1>Сәлем, Айгүл! <span className="wave">✦</span></h1>
              <p className="welcome-copy">Бүгін де бірге сөйлесуге бір қадам жақындайық.</p>
            </div>
            <span className="date-chip"><span className="date-dot" /> Бүгін, 24 қазан</span>
          </section>

          <section className="hero-card">
            <div className="hero-copy">
              <span className="hero-kicker">АСЫЛЫМНЫҢ БҮГІНГІ КҮНІ</span>
              <h2>Әр ойы маңызды. Әр сөзі құнды.</h2>
              <p>Таныс карточкалармен тілдесіп, бірге жаңа сөздер ашыңыз.</p>
              <div className="hero-actions">
                <button className="button-primary" onClick={() => announce("Сөйлесу режимі іске қосылды")}><Icon name="message" size={16} /> Сөйлесу режимін ашу</button>
                <button className="button-secondary" onClick={() => announce("Жоспар әзірленуде")}><Icon name="calendar" size={16} /> Күн тәртібі</button>
              </div>
            </div>
            <div className="hero-art" aria-hidden="true">
              <span className="art-sparkle sparkle-one">✳</span>
              <span className="art-bubble bubble-back"><Icon name="chat" size={27} /></span>
              <span className="art-bubble bubble-front"><Icon name="message" size={22} /></span>
              <span className="art-dot dot-one" /><span className="art-dot dot-two" />
            </div>
          </section>

          <section className="stats-grid" aria-label="Бүгінгі көрсеткіштер">
            <article className="stat-card stat-blue">
              <div className="stat-top"><span>БҮГІН АЙТЫЛҒАН СӨЗ</span><span className="stat-icon"><Icon name="message" size={17} /></span></div>
              <strong>24</strong><p>Кешеден 6 сөз артық</p><div className="stat-progress"><span style={{ width: "68%" }} /></div>
            </article>
            <article className="stat-card stat-green">
              <div className="stat-top"><span>СӨЙЛЕСУ УАҚЫТЫ</span><span className="stat-icon"><Icon name="chart" size={17} /></span></div>
              <strong>12 <small>минут</small></strong><p>Апталық ортадан жоғары</p><div className="stat-progress"><span style={{ width: "52%" }} /></div>
            </article>
            <article className="stat-card stat-peach">
              <div className="stat-top"><span>ЖАҢА СӨЗДЕР</span><span className="stat-icon"><Icon name="sparkles" size={17} /></span></div>
              <strong>3 <small>жаңа сөз</small></strong><p>Осы аптада үйренді</p><div className="stat-tags"><span>Су</span><span>Көкөніс</span><span>Ойнау</span></div>
            </article>
          </section>

          <section className="section-block children-section">
            <div className="section-heading">
              <div><p className="eyebrow">БАЛАҢЫЗДЫҢ ЖЕТІСТІГІ</p><h2>Балалар профилдері</h2></div>
              <button className="text-action" onClick={addChild}><Icon name="plus" size={15} /> Бала қосу</button>
            </div>
            <div className="children-grid">
              {children.map((child) => (
                <button key={child.name} className={`child-card${selectedChild === child.name ? " selected" : ""}`} onClick={() => setSelectedChild(child.name)}>
                  <span className={`avatar child-avatar ${child.color}`}>{child.initials}</span>
                  <span className="child-info"><strong>{child.name}</strong><small>{child.detail}</small><em>{selectedChild === child.name ? "Таңдалған профиль" : "Профильді ашу"} <Icon name="arrow" size={12} /></em></span>
                  <span className="child-check">{selectedChild === child.name ? "✓" : <Icon name="chevron" size={15} />}</span>
                </button>
              ))}
            </div>
          </section>

          <section className="section-block cards-section">
            <div className="section-heading">
              <div><p className="eyebrow">БІРГЕ ҮЙРЕНУГЕ ДАЙЫН</p><h2>Жақында қосылған карточкалар</h2></div>
              <button className="text-action" onClick={() => { setActivePage("Карточкалар кітапханасы"); announce("Карточкалар кітапханасы әзірленуде"); }}>Кітапханаға өту <Icon name="arrow" size={14} /></button>
            </div>
            <div className="cards-grid">
              {cards.map((card) => (
                <button key={card.name} className="picture-card" onClick={() => announce(`«${card.name}» карточкасы таңдалды`)}>
                  <span className={`picture-art ${card.tone}`}><span>{card.emoji}</span></span>
                  <strong>{card.name}</strong><small>{card.category}</small>
                </button>
              ))}
            </div>
          </section>

          <section className="quick-actions">
            <button className="quick-card" onClick={() => { setActivePage("ЖИ генераторы"); announce("Жаңа карточка генераторы әзірленуде"); }}>
              <span className="quick-icon quick-lilac"><Icon name="sparkles" size={20} /></span>
              <span><strong>Жаңа карточка жасау</strong><small>ЖИ көмегімен балаңызға таныс сурет жасаңыз.</small></span>
              <Icon name="arrow" size={16} />
            </button>
            <button className="quick-card" onClick={() => { setActivePage("Карточкалар жинағы"); announce("Карточкалар жинағы әзірленуде"); }}>
              <span className="quick-icon quick-mint"><Icon name="folder" size={20} /></span>
              <span><strong>Карточкалар жинағы</strong><small>Күнделікті қажет сөздерді бір жерге жинаңыз.</small></span>
              <Icon name="arrow" size={16} />
            </button>
          </section>
          <footer className="page-footer">Кішкентай қадамдар — үлкен жетістіктер <span>♥</span></footer>
        </div>
      </main>
      {notice && <div className="toast" role="status">{notice}</div>}
    </div>
  );
}