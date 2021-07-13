const productSelector = document.querySelector("#select-product")
const releaseSelector = document.querySelector("#select-release")
const addFwButton = document.querySelector("#btn-add-fw-rel")
const getDataButton = document.querySelector("#btn-get-data")
const fwRelTableBody = document.querySelector("#table-fw-rel > tbody")

let listsOfFws = []
const maxLimitForFw = 10

//=====
let grid;
let data = [];
const gridOptions = {
    enableCellNavigation: true,
    enableColumnReorder: true    
};


productSelector.addEventListener("change", productSelectListener)
addFwButton.addEventListener("click", addFwRelListener)
getDataButton.addEventListener("click", getData)

function fetchProducts(){
    fetch("products/")
    .then(res => res.json())
    .then(data => {data.forEach((product) => renderProduct(product))})
}

function renderProduct(product){
    el = document.createElement("option");
    el.setAttribute("value", product.id);
    el.text = product.name;
    productSelector.appendChild(el);
}

function fetchReleases(productId){
    fetch(`releases/${productId}`)
    .then(res => res.json())
    .then(data => {data.forEach((release) => renderRelease(release))})
}

function renderRelease(release){
    el = document.createElement("option");
    el.setAttribute("value", release.id);
    el.text = release.fw_version;
    releaseSelector.appendChild(el)
}
function clearReleases(){
    releaseSelector.options.length = 0
}

function productSelectListener(){
    clearReleases()
    if (productSelector.value != 0){
        fetchReleases(productSelector.value)
    }
}
 
function addFwRelListener(){
   product = productSelector.selectedOptions[0].text
   
   for(let i = 0; i < releaseSelector.selectedOptions.length; i++){
       const item  = {"product": product, 
       "fwRel": releaseSelector.selectedOptions[i].text, 
       "id": releaseSelector.selectedOptions[i].value }
        if (listsOfFws.length < 10){
            listsOfFws.push(item);
            renderRowInTable(item, listsOfFws.length)
        }else{
            alert(`Maximum ${maxLimitForFw} fw release can be added to the list`)
            // @TODO shall we disable btn-add-rel button or not ? 
            break;
        }
   }
}

function renderRowInTable(data, index){
    const tr = document.createElement("tr");
    tr.setAttribute('value', data.id);

    const th = document.createElement("th")
    th.setAttribute("scope", "row")
    th.innerText = index
    tr.appendChild(th)

    const product = document.createElement("td");
    product.innerText = data.product;
    tr.appendChild(product);

    const fwRel = document.createElement("td");
    fwRel.innerText = data.fwRel;
    tr.appendChild(fwRel);
    
    const deleteIcon = document.createElement("td");
    deleteIcon.innerHTML = '<a class="delete" title="Delete" data-toggle="tooltip"><i class="bi bi-trash"></a>';
    tr.appendChild(deleteIcon);

    fwRelTableBody.appendChild(tr);
    
    //add event listener on newly added delete icons
    const trashIcons = document.querySelectorAll(".delete");
    trashIcons[trashIcons.length-1].addEventListener("click", deleteRowListerner);
}

function deleteRowListerner(){
    const row = this.closest('tr')
    const newlist = listsOfFws.filter((item) => item.id !== row.getAttribute("value"));
    listsOfFws = newlist
    row.remove();
}

function getData(){
    console.log(listsOfFws)
    const ids = listsOfFws.map((item) => item.id)
    query = new URLSearchParams({"fws":ids}).toString()
    fetch(`testresults\?${query}`)
    .then(res => res.json())
    .then(data =>  {
        console.log(data)
        grid = new Slick.Grid("#myGrid", data.data, data.columns, gridOptions);
    })
}

fetchProducts();

