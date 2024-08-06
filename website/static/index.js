function deleteAlgorithm(algoID){
    fetch("/delete-algorithm",{
        method : "POST",
        body : JSON.stringify({algoID: algoID})
    }).then((_res) => {window.location.href = "/";});
}