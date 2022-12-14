let  genChart = (purchaseData, results) =>{
    let labels = [
        "Best Customers","Loyal Customers",
        "Big Spender", "Almost Lost", 
        "Lost Customers","Lost Cheap Customers"
    ]
    let data = [
        purchaseData[0]["Best_Customers"],purchaseData[0]["Loyal_Customers"],
        purchaseData[0]["Big_Spender"],purchaseData[0]["Almost_Lost"],
        purchaseData[0]["Lost_Customers"],purchaseData[0]["Lost_Cheap_Customers"]

    ]
    let colors = [
        "rgba(255,99,132,1)","rgba(54,162,235,1)",
        "rgba(255,206,86,1)","rgba(153,86,192,1)",
        "rgba(255,159,64,1)","rgba(25,159,64,1)",
    ]

    let CustomersChart =  document.getElementById("CustomersChart")
    let massPopChart = new Chart(CustomersChart,{
        type:"bar",
        data:{
            labels: labels,
            datasets:[{
                label:"Amount Of Customers Per Label",
                data:data,
                backgroundColor:colors
                
            }]
        },
        options:{

        }
    })

    let genTableRow = (customerId, cluster) =>{
        let tr = document.createElement("tr")
        let th = document.createElement("th")
        let td =  document.createElement("td")
        let b = document.createElement("b")
        b.setAttribute("class", "cluster-label")
        td.appendChild(b)

        cluster = cluster.toString()
        b.innerHTML = "Cluster " + cluster
        th.innerHTML = customerId
        if (cluster === "0"){
            b.style.backgroundColor = "red" 
        }
        else if (cluster === "1"){
            b.style.backgroundColor = "lightseagreen"
        }
        else if (cluster === "2"){
            b.style.backgroundColor = "limegreen"
        }
        else if (cluster === "3"){
            b.style.backgroundColor = "purple"

        }
        else if(cluster === "4"){
            b.style.backgroundColor = "orangered"
        }
        tr.append(th, td)
        return tr
    }

    let genTable = (results) =>{
        let resultCard = document.querySelector(".result-clusters")
        for (let i = 0; i <= 50; i++){
            let tableRow = genTableRow(results["CustomerID"][`${i}`],results["Cluster"][`${i}`] )
            resultCard.append(tableRow)
        } 
    }
    genTable(results)
    AOS.init({
        duration: 1000,
        easing: "ease-in-out",
        once: true,
        mirror: false,
        disable:"mobile"
    })
}