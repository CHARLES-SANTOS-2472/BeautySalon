document.getElementById("btnAPI").onclick = async () => {

    const resposta = await fetch("http://127.0.0.1:5000/");

    const dados = await resposta.json();

    console.log(dados);

    alert(dados.sistema);
}