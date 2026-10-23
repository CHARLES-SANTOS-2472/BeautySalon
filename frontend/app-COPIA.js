const formLogin = document.getElementById("formLogin");
const telaLogin = document.getElementById("telaLogin");
const telaDashboard = document.getElementById("telaDashboard");
const mensagemLogin = document.getElementById("mensagemLogin");
const mensagemDashboard = document.getElementById("mensagemDashboard");
const btnSair = document.getElementById("btnSair");
const btnAtualizar = document.getElementById("btnAtualizar");
const apiUrlInput = document.getElementById("apiUrl");
const btnAbrirSenha = document.getElementById("btnAbrirSenha");
const painelSenha = document.getElementById("painelSenha");
const formSenha = document.getElementById("formSenha");
const mensagemSenha = document.getElementById("mensagemSenha");
const btnAlterarSenha = document.getElementById("btnAlterarSenha");
const modalSenha = document.getElementById("modalSenha");
const formAlterarSenha = document.getElementById("formAlterarSenha");
const btnCancelarSenha = document.getElementById("btnCancelarSenha");




const moeda = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});

apiUrlInput.value = localStorage.getItem("beautySalonApiUrl")
    || "http://127.0.0.1:5000";

function obterApiUrl() {
    return apiUrlInput.value.trim().replace(/\/$/, "");
}

function mostrarMensagem(elemento, texto, erro = false) {
    elemento.textContent = texto;
    elemento.classList.toggle("erro", erro);
}

async function requisicao(endpoint, opcoes = {}) {
    const token = localStorage.getItem("beautySalonToken");

    const resposta = await fetch(`${obterApiUrl()}${endpoint}`, {
        ...opcoes,
        headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...(opcoes.headers || {})
        }
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro || dados.msg || "Não foi possível carregar os dados.");
    }

    return dados;
}

function preencherRanking(idLista, itens, textoQuantidade) {
    const lista = document.getElementById(idLista);
    lista.innerHTML = "";

    if (!itens.length) {
        lista.innerHTML = "<li>Nenhum dado disponível.</li>";
        return;
    }

    itens.forEach((item) => {
        const linha = document.createElement("li");
        const nome = document.createElement("span");
        const quantidade = document.createElement("strong");

        nome.textContent = item.servico || item.produto;
        quantidade.textContent = textoQuantidade(item);

        linha.append(nome, quantidade);
        lista.appendChild(linha);
    });
}

async function carregarDashboard() {
    try {
        mostrarMensagem(mensagemDashboard, "Carregando dados...");
        const dados = await requisicao("/dashboard/completo");

        const indicadores = dados.indicadores_gerais;

        document.getElementById("clientes").textContent = indicadores.clientes;
        document.getElementById("funcionarios").textContent = indicadores.funcionarios;
        document.getElementById("agendamentos").textContent = dados.agendamentos.total;
        document.getElementById("agendamentosHoje").textContent = dados.agendamentos.hoje;
        document.getElementById("vendas").textContent = indicadores.vendas;
        document.getElementById("faturamento").textContent =
            moeda.format(indicadores.faturamento_total);

        document.getElementById("estoqueBaixo").textContent =
            dados.estoque.produtos_estoque_baixo;

        preencherRanking(
            "listaServicos",
            dados.servicos_mais_realizados,
            (item) => `${item.quantidade} realizados`
        );

        preencherRanking(
            "listaProdutos",
            dados.produtos_mais_vendidos,
            (item) => `${item.quantidade_vendida} vendidos`
        );

        mostrarMensagem(mensagemDashboard, "");
    } catch (erro) {
        mostrarMensagem(mensagemDashboard, erro.message, true);
    }
}

function mostrarDashboard() {
    telaLogin.classList.add("escondido");
    telaDashboard.classList.remove("escondido");
    btnSair.classList.remove("escondido");
    btnAbrirSenha.classList.remove("escondido");
    btnAbrirSenha.classList.add("escondido");
    painelSenha.classList.add("escondido");
    btnAlterarSenha.classList.remove("escondido");
    btnAlterarSenha.classList.add("escondido");
    carregarDashboard();
}

formLogin.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    try {
        mostrarMensagem(mensagemLogin, "Entrando...");

        const resposta = await fetch(`${obterApiUrl()}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: document.getElementById("email").value,
                senha: document.getElementById("senha").value
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || "Não foi possível entrar.");
        }

        localStorage.setItem("beautySalonToken", dados.access_token);
        localStorage.setItem("beautySalonApiUrl", obterApiUrl());

        mostrarDashboard();
    } catch (erro) {
        mostrarMensagem(mensagemLogin, erro.message, true);
    }
});

btnAtualizar.addEventListener("click", carregarDashboard);

btnSair.addEventListener("click", () => {
    localStorage.removeItem("beautySalonToken");
    telaDashboard.classList.add("escondido");
    telaLogin.classList.remove("escondido");
    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");
    painelSenha.classList.add("escondido");
});

if (localStorage.getItem("beautySalonToken")) {
    mostrarDashboard();
}




btnAbrirSenha.addEventListener("click", () => {
    painelSenha.classList.toggle("escondido");
    mostrarMensagem(mensagemSenha, "");
});

formSenha.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const senhaAtual = document.getElementById("senhaAtual").value;
    const novaSenha = document.getElementById("novaSenha").value;
    const confirmarNovaSenha =
        document.getElementById("confirmarNovaSenha").value;

    if (novaSenha !== confirmarNovaSenha) {
        mostrarMensagem(
            mensagemSenha,
            "A confirmação da nova senha não confere.",
            true
        );
        return;
    }

    try {
        const dados = await requisicao("/alterar-senha", {
            method: "PUT",
            body: JSON.stringify({
                senha_atual: senhaAtual,
                nova_senha: novaSenha,
                confirmar_nova_senha: confirmarNovaSenha
            })
        });

        mostrarMensagem(mensagemSenha, dados.mensagem);
        formSenha.reset();
        painelSenha.classList.add("escondido");
    } catch (erro) {
        mostrarMensagem(mensagemSenha, erro.message, true);
    }
});




btnAlterarSenha.addEventListener("click", () => {
    formAlterarSenha.reset();
    mostrarMensagem(mensagemSenha, "");
    modalSenha.classList.remove("escondido");
});

btnCancelarSenha.addEventListener("click", () => {
    modalSenha.classList.add("escondido");
});

formAlterarSenha.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    try {
        mostrarMensagem(mensagemSenha, "Alterando senha...");

        const dados = await requisicao("/alterar-senha", {
            method: "PUT",
            body: JSON.stringify({
                senha_atual: document.getElementById("senhaAtual").value,
                nova_senha: document.getElementById("novaSenha").value,
                confirmar_nova_senha:
                    document.getElementById("confirmarNovaSenha").value
            })
        });

        localStorage.removeItem("beautySalonToken");
        modalSenha.classList.add("escondido");
        telaDashboard.classList.add("escondido");
        telaLogin.classList.remove("escondido");
        btnSair.classList.add("escondido");
        btnAlterarSenha.classList.add("escondido");

        mostrarMensagem(
            mensagemLogin,
            dados.mensagem + " Entre novamente com a nova senha."
        );
    } catch (erro) {
        mostrarMensagem(mensagemSenha, erro.message, true);
    }
});