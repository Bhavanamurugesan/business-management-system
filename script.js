function searchTable() {

    let input = document.getElementById("searchInput");

    let filter = input.value.toUpperCase();

    let table = document.querySelector("table");

    let tr = table.getElementsByTagName("tr");

    for(let i = 1; i < tr.length; i++){

        let td = tr[i].getElementsByTagName("td")[1];

        if(td){

            let textValue = td.textContent || td.innerText;

            if(textValue.toUpperCase().indexOf(filter) > -1){

                tr[i].style.display = "";

            }
            else{

                tr[i].style.display = "none";

            }
        }
    }
}


function darkMode(){

    document.body.classList.toggle("dark-mode");

}