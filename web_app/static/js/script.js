let currentLanguage = 'PT';

const translations = {
    'PT': {
        'tag-decodificacao': '[ DECODIFICAÇÃO DE SISTEMA VITAL ]',
        'hero-title': 'Seu Destino Não É Um Acaso.<br>Ele É Um Algoritmo.',
        'hero-subtitle': 'A 01GURU une a precisão cirúrgica dos dados astrofísicos com a milenar ciência da numerologia. Descubra o código secreto gravado no seu nascimento que rege sua carreira, relacionamentos e propósito de vida. Em menos de 30 segundos.',
        'cta-button': '[ DECODIFICAR MEU MAPA PESSOAL ]',
        'form-title': 'Terminal de Inserção de Parâmetros',
        'label-nome': 'NOME COMPLETO DO ALVO',
        'label-data': 'DATA DE NASCIMENTO',
        'label-hora': 'HORA EXATA',
        'label-pais': 'PAÍS',
        'label-estado': 'ESTADO (UF)',
        'label-cidade': 'CIDADE',
        'label-protocolo': 'SELECIONE O PROTOCOLO DE AUDITORIA',
        'opt-sel-pais': 'Selecione o País',
        'opt-aguarde-pais': 'Aguardando País...',
        'opt-aguarde-estado': 'Aguardando Estado...',
        'btn-submit': '[ EXECUTAR DECIFRAMENTO ]',
        'alert-sel-protocol': 'Por favor, selecione um protocolo de auditoria.',
        'alert-concluido': 'Diagnóstico concluído e arquivo transferido. Verifique seus downloads.',
        'installments': '12x de ',
        // Placeholders
        'ph-nome': 'Digite seu nome completo...',
        'ph-hora': '00:00',
        // Authority Blocks
        'param-title': 'A Engenharia dos Seus Parâmetros',
        'param-name-title': 'Nome Completo',
        'param-name-desc': 'O identificador vibratório primário. O seu nome de batismo codifica o seu Número de Expressão e Desejo da Alma. É a frequência exata da sua assinatura no mundo.',
        'param-date-title': 'Data de Nascimento',
        'param-date-desc': 'O Código Fonte. Define o seu Caminho da Vida (Life Path) e ancora matematicamente os ciclos decenais de materialização financeira e provações kármicas.',
        'param-hour-title': 'Hora Exata',
        'param-hour-desc': 'O portal de ativação. Calibra o Ascendente (ASC). Sem a hora exata, a precisão do seu Firewall Energético cai drasticamente, criando pontos cegos na sua blindagem.',
        'param-loc-title': 'Cidade, Estado e País',
        'param-loc-desc': 'Coordenadas Geobiométricas. A posição planetária exata sobre o seu local de nascimento gera um Blueprint irreproduzível. Essencial para a triangulação de trânsitos e oportunidades.',
        'genesis-title': 'A Gênese do 01GURU',
        'genesis-p1': 'O 01GURU não é uma consultoria mística; é um Gabinete de Inteligência Humana e Vibracional. Nascemos da fusão brutal entre a lógica binária dos dados (01) e a precisão inegável dos ciclos cósmicos (GURU).',
        'genesis-p2': 'Sob a arquitetura de Gabriel Prado — Estrategista Sênior e Engenheiro de Operações — o sistema foi forjado para uma única missão: transformar o esoterismo passivo em uma ferramenta tática de materialização e lucro.',
        'genesis-p3': 'Não lemos o seu futuro para confortar o seu ego. Nós auditamos o seu sistema vital, debugamos as suas falhas repetitivas e entregamos a rota matemática exata para o topo.',
        'footer-exec': 'Documento Executivo | Op: Gabriel Prado Rodrigues | CRA-RS TE-002457/O',
        'link-privacy': 'Política de Privacidade',
        'link-sub': 'Gerenciar Assinatura'
    },
    'EN': {
        'tag-decodificacao': '[ VITAL SYSTEM DECODING ]',
        'hero-title': 'Design Your Future.<br>Audit Your Reality.',
        'hero-subtitle': '01GURU merges astrophysical precision with high-dimensional numerology. Access the encrypted blueprint assigned to you at birth. Optimize your career, legacy, and tactical choices. Instant delivery.',
        'cta-button': '[ ACCESS MY TACTICAL BLUEPRINT ]',
        'form-title': 'Parameter Insertion Terminal',
        'label-nome': 'FULL TARGET NAME',
        'label-data': 'DATE OF BIRTH',
        'label-hora': 'EXACT TIME',
        'label-pais': 'COUNTRY',
        'label-estado': 'STATE / PROVINCE',
        'label-cidade': 'CITY',
        'label-protocolo': 'SELECT AUDIT PROTOCOL',
        'opt-sel-pais': 'Select Country',
        'opt-aguarde-pais': 'Waiting for Country...',
        'opt-aguarde-estado': 'Waiting for State...',
        'btn-submit': '[ EXECUTE DECODING ]',
        'alert-sel-protocol': 'Please select an audit protocol.',
        'alert-concluido': 'Diagnosis complete. Tactical file transferred. Check your downloads.',
        'installments': 'One-time payment',
        // Authority Blocks
        'param-title': 'The Engineering of Your Parameters',
        'param-name-title': 'Full Name',
        'param-name-desc': 'The primary vibrational identifier. Your birth name encodes your Soul Expression and Desire Number. It is the exact frequency of your signature in the world.',
        'param-date-title': 'Date of Birth',
        'param-date-desc': 'The Source Code. Defines your Life Path and mathematically anchors decennial cycles of financial materialization and karmic trials.',
        'param-hour-title': 'Exact Time',
        'param-hour-desc': 'The activation portal. Calibrates the Ascendant (ASC). Without the exact hour, the precision of your Personal Firewall drops drastically, creating blind spots in your shielding.',
        'param-loc-title': 'City, State, and Country',
        'param-loc-desc': 'Geobiometric Coordinates. The exact planetary position over your birth location generates an irreproducible Blueprint. Essential for transit triangulation.',
        'genesis-title': 'The Genesis of 01GURU',
        'genesis-p1': '01GURU is not a mystical consultancy; it is a Human and Vibrational Intelligence Cabinet. We were born from the brutal fusion between binary logic (01) and the undeniable precision of cosmic cycles (GURU).',
        'genesis-p2': 'Under the architecture of Gabriel Prado — Senior Strategist and Operations Engineer — the system was forged for a single mission: to transform passive esoterism into a tactical tool for manifestation and profit.',
        'genesis-p3': 'We do not read your future to comfort your ego. We audit your vital system, debug your repetitive failures, and deliver the exact mathematical route to the top.',
        'footer-exec': 'Executive Document | Op: Gabriel Prado Rodrigues | CRA-RS TE-002457/O',
        'link-privacy': 'Privacy Policy',
        'link-sub': 'Manage Subscription'
    }
};

const countries = [
    "Brasil", "United States", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. 'Swaziland')", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
];

function scrollToTerminal() {
    const terminal = document.getElementById('terminal-section');
    terminal.classList.remove('hidden');
    void terminal.offsetWidth; 
    terminal.classList.remove('opacity-0');
    terminal.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(() => { document.getElementById('nome').focus(); }, 500);
}

function scrollToForm() {
    scrollToTerminal();
}

function setLanguage(lang) {
    currentLanguage = lang;
    
    // Update Toggle Buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent === lang);
    });

    // Update Text Content
    for (let id in translations[lang]) {
        const el = document.getElementById(id);
        if (el) {
            if (id === 'hero-title') el.innerHTML = translations[lang][id];
            else el.textContent = translations[lang][id];
        }
    }

    // Update Placeholders
    document.getElementById('nome').placeholder = translations[lang]['ph-nome'] || '';
    document.getElementById('horaNascimento').placeholder = translations[lang]['ph-hora'] || '';

    // Update Protocol Cards Copy
    document.querySelectorAll('.protocol-card').forEach(card => {

        const title = card.querySelector('.card-title');
        const desc = card.querySelector('.card-desc');
        if (title) title.textContent = title.dataset[lang.toLowerCase()];
        if (desc) desc.textContent = desc.dataset[lang.toLowerCase()];
    });

    updatePrices();
}

function updatePrices() {
    const paísValue = document.getElementById('pais').value;
    const isBrazil = paísValue === 'Brasil';
    const lang = currentLanguage;

    document.querySelectorAll('.protocol-card').forEach(card => {
        const priceEl = card.querySelector('.card-price');
        if (!priceEl) return;

        const brl = parseFloat(priceEl.dataset.brl);
        const usd = parseFloat(priceEl.dataset.usd);

        if (isNaN(brl)) return;

        if (isBrazil && lang === 'PT') {
            const installment = (brl / 12).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
            const cash = brl.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
            priceEl.innerHTML = `12x de ${installment}<br><small>ou ${cash} à vista</small>`;
        } else {
            // EN mode or Non-Brazil always shows USD
            const prefix = lang === 'PT' ? 'Preço: ' : 'Price: ';
            priceEl.textContent = `${prefix}$ ${usd.toFixed(2)} USD`;
        }
    });
}




// Location Dropdown Logic (IBGE API for Brazil)
async function loadStates() {
    const estadoSelect = document.getElementById('estado');
    const cidadeSelect = document.getElementById('cidade');
    
    try {
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome');
        const states = await response.json();
        
        const lang = currentLanguage;
        estadoSelect.innerHTML = `<option value="">${translations[lang]['opt-aguarde-pais']}</option>`;
        
        if (document.getElementById('pais').value === 'Brasil') {
            estadoSelect.innerHTML = `<option value="">${lang === 'PT' ? 'Selecione o Estado' : 'Select State'}</option>`;
            states.forEach(state => {
                const option = document.createElement('option');
                option.value = state.sigla;
                option.textContent = `${state.nome} (${state.sigla})`;
                option.dataset.id = state.id;
                estadoSelect.appendChild(option);
            });
            estadoSelect.disabled = false;
        } else {
            // USA/Other Fallback - simplified for now
            estadoSelect.innerHTML = '<option value="OTHER">Other/External</option>';
            estadoSelect.disabled = false;
            loadCities('OTHER');
        }
        
        estadoSelect.addEventListener('change', (e) => {
            const stateId = e.target.options[e.target.selectedIndex].dataset.id;
            if (stateId) {
                loadCities(stateId);
            } else if (e.target.value === 'OTHER') {
                loadCities('OTHER');
            }
        });
        
        updatePrices();
    } catch (err) {
        console.error("Error loading states:", err);
    }
}

document.getElementById('pais').addEventListener('change', (e) => {
    const val = e.target.value;
    if (val === 'United States' || val === 'United States of America') setLanguage('EN');
    else if (val === 'Brasil') setLanguage('PT');
    loadStates();
});



async function loadCities(stateId) {
    const cidadeSelect = document.getElementById('cidade');
    const lang = currentLanguage;

    if (stateId === 'OTHER') {
        cidadeSelect.innerHTML = `<option value="External">${lang === 'PT' ? 'Cidade Externa' : 'External City'}</option>`;
        cidadeSelect.disabled = false;
        return;
    }

    cidadeSelect.innerHTML = `<option value="">${lang === 'PT' ? 'Carregando...' : 'Loading...'}</option>`;
    cidadeSelect.disabled = true;
    
    try {
        const response = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${stateId}/municipios?orderBy=nome`);
        const cities = await response.json();
        
        cidadeSelect.innerHTML = `<option value="">${lang === 'PT' ? 'Selecione a Cidade' : 'Select City'}</option>`;
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.nome;
            option.textContent = city.nome;
            cidadeSelect.appendChild(option);
        });
        
        cidadeSelect.disabled = false;
    } catch (err) {
        console.error("Error loading cities:", err);
    }
}




function selectProtocol(id) {
    // Unselect all
    document.querySelectorAll('.protocol-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Select the clicked one
    const card = document.querySelector(`.protocol-card[onclick="selectProtocol('${id}')"]`);
    if (card) {
        card.classList.add('selected');
        const radio = card.querySelector('input[type="radio"]');
        if (radio) radio.checked = true;
    }
}


document.getElementById('dossie-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const selectedProtocol = document.querySelector('input[name="protocolo"]:checked')?.value;
    
    if (!selectedProtocol) {
        alert("Por favor, selecione um protocolo de auditoria.");
        return;
    }

    const formData = {
        nome: document.getElementById('nome').value,
        dataNascimento: document.getElementById('dataNascimento').value,
        horaNascimento: document.getElementById('horaNascimento').value,
        cidade: document.getElementById('cidade').value,
        estado: document.getElementById('estado').value,
        protocolo: selectedProtocol,
        idioma: currentLanguage
    };



    // Show Loading Overlay
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('hidden');
    
    // Start fake terminal logs sequence
    runTerminalAnimSequence();

    try {
        const response = await fetch('/api/gerar_dossie', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.erro || 'Erro desconhecido');
        }

        // Handle File Download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        let protocolName = formData.protocolo === "16" ? "DOSSIE_GOD_MODE" : "RELATORIO_TATICO";
        let sanitizedName = formData.nome.split(' ')[0].toUpperCase();
        a.download = `01GURU_${protocolName}_${sanitizedName}.pdf`;
        
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        a.remove();
        
        // Reset and hide overlay
        setTimeout(() => {
            overlay.classList.add('hidden');
            alert(translations[currentLanguage]['alert-concluido']);
        }, 1000);


    } catch (error) {
        console.error('Error:', error);
        alert('FALHA DE SISTEMA: ' + error.message);
        overlay.classList.add('hidden');
    }
});


window.onload = () => {
    populateCountries();
    loadStates();
    selectProtocol('16');
    setLanguage('PT');
};

function populateCountries() {
    const paisSelect = document.getElementById('pais');
    paisSelect.innerHTML = '<option value="" id="opt-sel-pais">Selecione o País</option>';
    countries.sort().forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        if (c === 'Brasil') opt.selected = true;
        paisSelect.appendChild(opt);
    });
}

