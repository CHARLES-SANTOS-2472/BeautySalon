const formLogin = document.getElementById("formLogin");
const formSenha = document.getElementById("formSenha");
const formSolicitarCodigo = document.getElementById("formSolicitarCodigo");
const formRedefinirSenha = document.getElementById("formRedefinirSenha");
const formCliente = document.getElementById("formCliente");
const formFuncionario = document.getElementById("formFuncionario");
const formCategoria = document.getElementById("formCategoria");


const telaLogin = document.getElementById("telaLogin");
const telaSenha = document.getElementById("telaSenha");
const telaDashboard = document.getElementById("telaDashboard");
const telaClientes = document.getElementById("telaClientes");
const telaFuncionarios = document.getElementById("telaFuncionarios");
const telaFormularioFuncionario = document.getElementById("telaFormularioFuncionario");
const telaCategorias = document.getElementById("telaCategorias");
const telaFormularioCategoria = document.getElementById("telaFormularioCategoria");


const telaRecuperarSenha = document.getElementById(
    "telaRecuperarSenha"
);

const telaFormularioCliente = document.getElementById(
    "telaFormularioCliente"
);

const etapaSolicitarCodigo = document.getElementById("etapaSolicitarCodigo");
const etapaRedefinirSenha = document.getElementById("etapaRedefinirSenha");

const mensagemLogin = document.getElementById("mensagemLogin");
const mensagemSenha = document.getElementById("mensagemSenha");
const mensagemDashboard = document.getElementById("mensagemDashboard");
const mensagemClientes = document.getElementById("mensagemClientes");
const mensagemFuncionarios = document.getElementById("mensagemFuncionarios");
const mensagemFormularioFuncionario = document.getElementById("mensagemFormularioFuncionario");
const mensagemCategorias = document.getElementById("mensagemCategorias");
const mensagemFormularioCategoria = document.getElementById("mensagemFormularioCategoria");


const mensagemRecuperacao = document.getElementById("mensagemRecuperacao");
const mensagemRedefinirSenha = document.getElementById("mensagemRedefinirSenha");
const mensagemFormularioCliente = document.getElementById("mensagemFormularioCliente");

const btnSair = document.getElementById("btnSair");
const btnAbrirSenha = document.getElementById("btnAbrirSenha");
const btnCancelarSenha = document.getElementById("btnCancelarSenha");
const btnAtualizar = document.getElementById("btnAtualizar");
const btnAtualizarClientes = document.getElementById("btnAtualizarClientes");
const btnNovoCliente = document.getElementById("btnNovoCliente");
const btnNovoFuncionario = document.getElementById("btnNovoFuncionario");
const btnAtualizarFuncionarios = document.getElementById("btnAtualizarFuncionarios");
const btnCancelarFormularioFuncionario = document.getElementById("btnCancelarFormularioFuncionario");
const btnNovaCategoria = document.getElementById("btnNovaCategoria");
const btnAtualizarCategorias = document.getElementById("btnAtualizarCategorias");
const btnCancelarFormularioCategoria = document.getElementById("btnCancelarFormularioCategoria");

const btnCancelarFormularioCliente = document.getElementById("btnCancelarFormularioCliente");
const btnEsqueciSenha = document.getElementById("btnEsqueciSenha");
const btnVoltarLogin = document.getElementById("btnVoltarLogin");
const btnCancelarRecuperacao = document.getElementById("btnCancelarRecuperacao");
const navegacaoPrincipal = document.getElementById("navegacaoPrincipal");
const navegacaoMobile = document.getElementById("navegacaoMobile");

const buscaCliente = document.getElementById("buscaCliente");
const listaClientes = document.getElementById("listaClientes");
const buscaFuncionario = document.getElementById("buscaFuncionario");
const listaFuncionarios = document.getElementById("listaFuncionarios");
const tituloFormularioFuncionario = document.getElementById("tituloFormularioFuncionario");
const listaCategorias = document.getElementById("listaCategorias");
const tituloFormularioCategoria = document.getElementById("tituloFormularioCategoria");
const tituloFormularioCliente = document.getElementById("tituloFormularioCliente");

const apiUrlInput = document.getElementById("apiUrl");

let clientes = [];
let clienteEditandoId = null;
let funcionarios = [];
let funcionarioEditandoId = null;
let categorias = [];
let categoriaEditandoId = null;

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


function mostrarNavegacao() {
    navegacaoPrincipal.classList.remove("escondido");
    navegacaoMobile.classList.remove("escondido");
}


function esconderNavegacao() {
    navegacaoPrincipal.classList.add("escondido");
    navegacaoMobile.classList.add("escondido");
}


function atualizarNavegacao(telaAtiva) {
    document.querySelectorAll("[data-tela]").forEach((botao) => {
        botao.classList.toggle(
            "ativo",
            botao.dataset.tela === telaAtiva
        );
    });
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
        throw new Error(
            dados.erro || dados.msg || "Não foi possível concluir a ação."
        );
    }

    return dados;
}


async function requisicaoPublica(endpoint, dados) {
    const resposta = await fetch(`${obterApiUrl()}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    });

    const respostaDados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(
            respostaDados.erro
            || respostaDados.msg
            || "Não foi possível concluir a solicitação."
        );
    }

    return respostaDados;
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

        document.getElementById("clientes").textContent =
            indicadores.clientes;

        document.getElementById("funcionarios").textContent =
            indicadores.funcionarios;

        document.getElementById("agendamentos").textContent =
            dados.agendamentos.total;

        document.getElementById("agendamentosHoje").textContent =
            dados.agendamentos.hoje;

        document.getElementById("vendas").textContent =
            indicadores.vendas;

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


function criarBotao(texto, classe, aoClicar) {
    const botao = document.createElement("button");

    botao.type = "button";
    botao.textContent = texto;
    botao.className = classe;
    botao.addEventListener("click", aoClicar);

    return botao;
}


function renderizarClientes() {
    const textoBusca = buscaCliente.value.trim().toLowerCase();

    const resultado = clientes.filter((cliente) => {
        const textoCliente = [
            cliente.nome,
            cliente.telefone,
            cliente.email
        ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

        return textoCliente.includes(textoBusca);
    });

    listaClientes.innerHTML = "";

    if (!resultado.length) {
        listaClientes.innerHTML = `
            <article class="cartao cliente-item">
                <p>Nenhum cliente encontrado.</p>
            </article>
        `;
        return;
    }

    resultado.forEach((cliente) => {
        const item = document.createElement("article");
        const nome = document.createElement("h3");
        const telefone = document.createElement("p");
        const email = document.createElement("p");
        const cpf = document.createElement("p");
        const acoes = document.createElement("div");

        item.className = "cartao cliente-item";
        acoes.className = "acoes-item";

        nome.textContent = cliente.nome;

        telefone.textContent =
            `Telefone: ${cliente.telefone || "Não informado"}`;

        email.textContent =
            `E-mail: ${cliente.email || "Não informado"}`;

        cpf.textContent =
            `CPF: ${cliente.cpf || "Não informado"}`;

        const btnEditar = criarBotao(
            "Editar",
            "botao-secundario",
            () => abrirFormularioCliente(cliente)
        );

        const btnDesativar = criarBotao(
            "Desativar",
            "botao-perigo",
            () => desativarCliente(cliente)
        );

        acoes.append(btnEditar, btnDesativar);
        item.append(nome, telefone, email, cpf, acoes);

        listaClientes.appendChild(item);
    });
}


async function carregarClientes() {
    try {
        mostrarMensagem(mensagemClientes, "Carregando clientes...");

        clientes = await requisicao("/clientes");

        renderizarClientes();

        mostrarMensagem(mensagemClientes, "");
    } catch (erro) {
        mostrarMensagem(mensagemClientes, erro.message, true);
    }
}



function renderizarFuncionarios() {
    const textoBusca = buscaFuncionario.value
        .trim()
        .toLowerCase();

    const resultado = funcionarios.filter((funcionario) => {
        const textoFuncionario = [
            funcionario.nome,
            funcionario.telefone,
            funcionario.cargo
        ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

        return textoFuncionario.includes(textoBusca);
    });

    listaFuncionarios.innerHTML = "";

    if (!resultado.length) {
        listaFuncionarios.innerHTML = `
            <article class="cartao funcionario-item">
                <p>Nenhum funcionário encontrado.</p>
            </article>
        `;
        return;
    }

    resultado.forEach((funcionario) => {
        const item = document.createElement("article");
        const nome = document.createElement("h3");
        const telefone = document.createElement("p");
        const cargo = document.createElement("p");
        const comissao = document.createElement("p");
        const status = document.createElement("p");
        const acoes = document.createElement("div");

        item.className = "cartao funcionario-item";
        acoes.className = "acoes-item";

        nome.textContent = funcionario.nome;

        telefone.textContent =
            `Telefone: ${funcionario.telefone || "Não informado"}`;

        cargo.textContent =
            `Cargo: ${funcionario.cargo || "Não informado"}`;

        comissao.textContent = funcionario.percentual_comissao === null
            ? "Comissão: Não informada"
            : `Comissão: ${funcionario.percentual_comissao}%`;

        status.textContent = funcionario.ativo
            ? "Status: Ativo"
            : "Status: Inativo";

        const btnEditar = criarBotao(
            "Editar",
            "botao-secundario",
            () => abrirFormularioFuncionario(funcionario)
        );

        const btnStatus = criarBotao(
            funcionario.ativo ? "Desativar" : "Ativar",
            funcionario.ativo ? "botao-perigo" : "botao-secundario",
            () => alterarStatusFuncionario(funcionario)
        );

        acoes.append(btnEditar, btnStatus);

        item.append(
            nome,
            telefone,
            cargo,
            comissao,
            status,
            acoes
        );

        listaFuncionarios.appendChild(item);
    });
}


async function carregarFuncionarios() {
    try {
        mostrarMensagem(
            mensagemFuncionarios,
            "Carregando funcionários..."
        );

        funcionarios = await requisicao("/funcionarios");

        renderizarFuncionarios();

        mostrarMensagem(mensagemFuncionarios, "");
    } catch (erro) {
        mostrarMensagem(
            mensagemFuncionarios,
            erro.message,
            true
        );
    }
}


async function mostrarFuncionarios() {
    esconderTelas();

    telaFuncionarios.classList.remove("escondido");

    btnSair.classList.remove("escondido");
    btnAbrirSenha.classList.remove("escondido");

    mostrarNavegacao();
    atualizarNavegacao("funcionarios");

    await carregarFuncionarios();
}




function esconderTelas() {
    telaLogin.classList.add("escondido");
    telaSenha.classList.add("escondido");
    telaDashboard.classList.add("escondido");
    telaClientes.classList.add("escondido");
    telaFuncionarios.classList.add("escondido");
    telaFormularioFuncionario.classList.add("escondido");
    telaCategorias.classList.add("escondido");
    telaFormularioCategoria.classList.add("escondido");
    telaRecuperarSenha.classList.add("escondido");
    telaFormularioCliente.classList.add("escondido");
}


function mostrarDashboard() {
    esconderTelas();

    telaDashboard.classList.remove("escondido");

    btnSair.classList.remove("escondido");
    btnAbrirSenha.classList.remove("escondido");

    mostrarNavegacao();
    atualizarNavegacao("dashboard");

    carregarDashboard();
}


async function mostrarClientes() {
    esconderTelas();

    telaClientes.classList.remove("escondido");

    btnSair.classList.remove("escondido");
    btnAbrirSenha.classList.remove("escondido");

    mostrarNavegacao();
    atualizarNavegacao("clientes");

    await carregarClientes();
}



function renderizarCategorias() {
    listaCategorias.innerHTML = "";

    if (!categorias.length) {
        listaCategorias.innerHTML = `
            <article class="cartao cliente-item">
                <p>Nenhuma categoria cadastrada.</p>
            </article>
        `;
        return;
    }

    categorias.forEach((categoria) => {
        const item = document.createElement("article");
        const nome = document.createElement("h3");
        const acoes = document.createElement("div");

        item.className = "cartao cliente-item";
        acoes.className = "acoes-item";

        nome.textContent = categoria.nome;

        const btnEditar = criarBotao(
            "Editar",
            "botao-secundario",
            () => abrirFormularioCategoria(categoria)
        );

        const btnExcluir = criarBotao(
            "Excluir",
            "botao-perigo",
            () => excluirCategoria(categoria)
        );

        acoes.append(btnEditar, btnExcluir);
        item.append(nome, acoes);

        listaCategorias.appendChild(item);
    });
}


async function carregarCategorias() {
    try {
        mostrarMensagem(
            mensagemCategorias,
            "Carregando categorias..."
        );

        categorias = await requisicao("/categorias-servico");

        renderizarCategorias();

        mostrarMensagem(mensagemCategorias, "");
    } catch (erro) {
        mostrarMensagem(
            mensagemCategorias,
            erro.message,
            true
        );
    }
}


async function mostrarCategorias() {
    esconderTelas();

    telaCategorias.classList.remove("escondido");

    btnSair.classList.remove("escondido");
    btnAbrirSenha.classList.remove("escondido");

    mostrarNavegacao();
    atualizarNavegacao("categorias");

    await carregarCategorias();
}


function mostrarLogin(mensagem = "") {
    esconderTelas();

    telaLogin.classList.remove("escondido");

    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");

    esconderNavegacao();

    mostrarMensagem(mensagemLogin, mensagem);
}


function abrirTelaSenha() {
    formSenha.reset();
    mostrarMensagem(mensagemSenha, "");

    esconderTelas();

    telaSenha.classList.remove("escondido");

    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");

    esconderNavegacao();
}


function voltarParaDashboard() {
    mostrarDashboard();
}


function abrirRecuperacaoSenha() {
    formSolicitarCodigo.reset();
    formRedefinirSenha.reset();

    mostrarMensagem(mensagemRecuperacao, "");
    mostrarMensagem(mensagemRedefinirSenha, "");

    etapaSolicitarCodigo.classList.remove("escondido");
    etapaRedefinirSenha.classList.add("escondido");

    esconderTelas();

    telaRecuperarSenha.classList.remove("escondido");

    esconderNavegacao();
}


function abrirFormularioCliente(cliente = null) {
    formCliente.reset();

    clienteEditandoId = cliente ? cliente.id : null;

    tituloFormularioCliente.textContent = cliente
        ? "Editar cliente"
        : "Novo cliente";

    mostrarMensagem(mensagemFormularioCliente, "");

    if (cliente) {
        document.getElementById("clienteNome").value =
            cliente.nome || "";

        document.getElementById("clienteCpf").value =
            cliente.cpf || "";

        document.getElementById("clienteTelefone").value =
            cliente.telefone || "";

        document.getElementById("clienteEmail").value =
            cliente.email || "";

        document.getElementById("clienteNascimento").value =
            cliente.data_nascimento || "";

        document.getElementById("clienteEndereco").value =
            cliente.endereco || "";

        document.getElementById("clienteObservacoes").value =
            cliente.observacoes || "";
    }

    esconderTelas();

    telaFormularioCliente.classList.remove("escondido");

    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");

    esconderNavegacao();
}









function abrirFormularioFuncionario(funcionario = null) {
    formFuncionario.reset();

    funcionarioEditandoId = funcionario
        ? funcionario.id
        : null;

    tituloFormularioFuncionario.textContent = funcionario
        ? "Editar funcionário"
        : "Novo funcionário";

    mostrarMensagem(mensagemFormularioFuncionario, "");

    if (funcionario) {
        document.getElementById("funcionarioNome").value =
            funcionario.nome || "";

        document.getElementById("funcionarioTelefone").value =
            funcionario.telefone || "";

        document.getElementById("funcionarioCargo").value =
            funcionario.cargo || "";

        document.getElementById("funcionarioComissao").value =
            funcionario.percentual_comissao ?? "";
    }

    esconderTelas();

    telaFormularioFuncionario.classList.remove("escondido");

    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");

    esconderNavegacao();
}


function abrirFormularioCategoria(categoria = null) {
    formCategoria.reset();

    categoriaEditandoId = categoria
        ? categoria.id
        : null;

    tituloFormularioCategoria.textContent = categoria
        ? "Editar categoria"
        : "Nova categoria";

    mostrarMensagem(mensagemFormularioCategoria, "");

    if (categoria) {
        document.getElementById("categoriaNome").value =
            categoria.nome || "";
    }

    esconderTelas();

    telaFormularioCategoria.classList.remove("escondido");

    btnSair.classList.add("escondido");
    btnAbrirSenha.classList.add("escondido");

    esconderNavegacao();
}


function montarDadosFuncionario() {
    const dados = {
        nome: document.getElementById("funcionarioNome").value.trim()
    };

    const telefone = document.getElementById(
        "funcionarioTelefone"
    ).value.trim();

    const cargo = document.getElementById(
        "funcionarioCargo"
    ).value.trim();

    const comissao = document.getElementById(
        "funcionarioComissao"
    ).value;

    if (telefone) {
        dados.telefone = telefone;
    }

    if (cargo) {
        dados.cargo = cargo;
    }

    if (comissao !== "") {
        dados.percentual_comissao = Number(comissao);
    }

    return dados;
}












function montarDadosCliente() {
    const dados = {
        nome: document.getElementById("clienteNome").value.trim()
    };

    const camposOpcionais = {
        cpf: "clienteCpf",
        telefone: "clienteTelefone",
        email: "clienteEmail",
        data_nascimento: "clienteNascimento",
        endereco: "clienteEndereco",
        observacoes: "clienteObservacoes"
    };

    Object.entries(camposOpcionais).forEach(([campo, id]) => {
        const valor = document.getElementById(id).value.trim();

        if (valor) {
            dados[campo] = valor;
        }
    });

    return dados;
}


async function desativarCliente(cliente) {
    const confirmar = window.confirm(
        `Deseja desativar o cliente "${cliente.nome}"?`
    );

    if (!confirmar) {
        return;
    }

    try {
        const dados = await requisicao(
            `/clientes/${cliente.id}`,
            {
                method: "DELETE"
            }
        );

        await mostrarClientes();

        mostrarMensagem(mensagemClientes, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(mensagemClientes, erro.message, true);
    }
}









async function alterarStatusFuncionario(funcionario) {
    const novoStatus = !funcionario.ativo;

    const acao = novoStatus
        ? "ativar"
        : "desativar";

    const confirmar = window.confirm(
        `Deseja ${acao} o funcionário "${funcionario.nome}"?`
    );

    if (!confirmar) {
        return;
    }

    try {
        const dados = await requisicao(
            `/funcionarios/${funcionario.id}`,
            {
                method: "PUT",
                body: JSON.stringify({
                    ativo: novoStatus
                })
            }
        );

        await mostrarFuncionarios();

        mostrarMensagem(mensagemFuncionarios, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemFuncionarios,
            erro.message,
            true
        );
    }
}




async function excluirCategoria(categoria) {
    const confirmar = window.confirm(
        `Deseja excluir a categoria "${categoria.nome}"?`
    );

    if (!confirmar) {
        return;
    }

    try {
        const dados = await requisicao(
            `/categorias-servico/${categoria.id}`,
            {
                method: "DELETE"
            }
        );

        await mostrarCategorias();

        mostrarMensagem(mensagemCategorias, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemCategorias,
            erro.message,
            true
        );
    }
}





function sair() {
    localStorage.removeItem("beautySalonToken");

    formSenha.reset();

    mostrarLogin();
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

btnAtualizarClientes.addEventListener("click", carregarClientes);

btnNovoCliente.addEventListener("click", () => {
    abrirFormularioCliente();
});






btnNovoFuncionario.addEventListener("click", () => {
    abrirFormularioFuncionario();
});

btnAtualizarFuncionarios.addEventListener(
    "click",
    carregarFuncionarios
);

btnCancelarFormularioFuncionario.addEventListener(
    "click",
    mostrarFuncionarios
);

buscaFuncionario.addEventListener(
    "input",
    renderizarFuncionarios
);


btnNovaCategoria.addEventListener("click", () => {
    abrirFormularioCategoria();
});

btnAtualizarCategorias.addEventListener(
    "click",
    carregarCategorias
);

btnCancelarFormularioCategoria.addEventListener(
    "click",
    mostrarCategorias
);











btnCancelarFormularioCliente.addEventListener("click", () => {
    mostrarClientes();
});

btnSair.addEventListener("click", sair);

btnAbrirSenha.addEventListener("click", abrirTelaSenha);

btnCancelarSenha.addEventListener("click", voltarParaDashboard);

btnEsqueciSenha.addEventListener("click", abrirRecuperacaoSenha);

btnVoltarLogin.addEventListener("click", () => {
    mostrarLogin();
});

btnCancelarRecuperacao.addEventListener("click", () => {
    mostrarLogin();
});

buscaCliente.addEventListener("input", renderizarClientes);


document.querySelectorAll("[data-tela]").forEach((botao) => {
    botao.addEventListener("click", () => {
        if (botao.dataset.tela === "dashboard") {
            mostrarDashboard();
        }

        if (botao.dataset.tela === "clientes") {
            mostrarClientes();
        }


        if (botao.dataset.tela === "funcionarios") {
            mostrarFuncionarios();
        }

        if (botao.dataset.tela === "categorias") {
            mostrarCategorias();
        }





    });
});


formCliente.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dadosCliente = montarDadosCliente();

    if (!dadosCliente.nome) {
        mostrarMensagem(
            mensagemFormularioCliente,
            "O nome é obrigatório.",
            true
        );
        return;
    }

    try {
        const endpoint = clienteEditandoId
            ? `/clientes/${clienteEditandoId}`
            : "/clientes";

        const metodo = clienteEditandoId
            ? "PUT"
            : "POST";

        const dados = await requisicao(endpoint, {
            method: metodo,
            body: JSON.stringify(dadosCliente)
        });

        await mostrarClientes();

        mostrarMensagem(mensagemClientes, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemFormularioCliente,
            erro.message,
            true
        );
    }
});




formFuncionario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dadosFuncionario = montarDadosFuncionario();

    if (!dadosFuncionario.nome) {
        mostrarMensagem(
            mensagemFormularioFuncionario,
            "O nome é obrigatório.",
            true
        );
        return;
    }

    try {
        const endpoint = funcionarioEditandoId
            ? `/funcionarios/${funcionarioEditandoId}`
            : "/funcionarios";

        const metodo = funcionarioEditandoId
            ? "PUT"
            : "POST";

        const dados = await requisicao(endpoint, {
            method: metodo,
            body: JSON.stringify(dadosFuncionario)
        });

        await mostrarFuncionarios();

        mostrarMensagem(mensagemFuncionarios, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemFormularioFuncionario,
            erro.message,
            true
        );
    }
});



formCategoria.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const nome = document.getElementById("categoriaNome").value
        .trim();

    if (!nome) {
        mostrarMensagem(
            mensagemFormularioCategoria,
            "O nome é obrigatório.",
            true
        );
        return;
    }

    try {
        const endpoint = categoriaEditandoId
            ? `/categorias-servico/${categoriaEditandoId}`
            : "/categorias-servico";

        const metodo = categoriaEditandoId
            ? "PUT"
            : "POST";

        const dados = await requisicao(endpoint, {
            method: metodo,
            body: JSON.stringify({
                nome: nome
            })
        });

        await mostrarCategorias();

        mostrarMensagem(mensagemCategorias, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemFormularioCategoria,
            erro.message,
            true
        );
    }
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
        mostrarMensagem(mensagemSenha, "Alterando senha...");

        const dados = await requisicao("/alterar-senha", {
            method: "PUT",
            body: JSON.stringify({
                senha_atual: senhaAtual,
                nova_senha: novaSenha,
                confirmar_nova_senha: confirmarNovaSenha
            })
        });

        voltarParaDashboard();

        mostrarMensagem(mensagemDashboard, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(mensagemSenha, erro.message, true);
    }
});


formSolicitarCodigo.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const email = document.getElementById("emailRecuperacao").value
        .trim()
        .toLowerCase();

    try {
        mostrarMensagem(mensagemRecuperacao, "Enviando código...");

        const dados = await requisicaoPublica("/esqueci-senha", {
            email: email
        });

        document.getElementById("emailRedefinir").value = email;

        etapaSolicitarCodigo.classList.add("escondido");
        etapaRedefinirSenha.classList.remove("escondido");

        mostrarMensagem(mensagemRedefinirSenha, dados.mensagem);
    } catch (erro) {
        mostrarMensagem(mensagemRecuperacao, erro.message, true);
    }
});


formRedefinirSenha.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const novaSenha = document.getElementById(
        "novaSenhaRecuperacao"
    ).value;

    const confirmarNovaSenha = document.getElementById(
        "confirmarSenhaRecuperacao"
    ).value;

    if (novaSenha !== confirmarNovaSenha) {
        mostrarMensagem(
            mensagemRedefinirSenha,
            "A confirmação da nova senha não confere.",
            true
        );
        return;
    }

    try {
        mostrarMensagem(
            mensagemRedefinirSenha,
            "Redefinindo senha..."
        );

        const dados = await requisicaoPublica("/redefinir-senha", {
            email: document.getElementById("emailRedefinir").value,
            codigo: document.getElementById("codigoRecuperacao").value,
            nova_senha: novaSenha,
            confirmar_nova_senha: confirmarNovaSenha
        });

        document.getElementById("email").value =
            document.getElementById("emailRedefinir").value;

        mostrarLogin(dados.mensagem);
    } catch (erro) {
        mostrarMensagem(
            mensagemRedefinirSenha,
            erro.message,
            true
        );
    }
});


if (localStorage.getItem("beautySalonToken")) {
    mostrarDashboard();
}