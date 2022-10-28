//大改1-4_1抓取屬性中的資料回填到姓名
let nameContent=document.getElementById("getName").getAttribute("d");
let nameBlock = document.createElement("div");     //创建一个div元素
let result_Name=document.createTextNode(nameContent+"歡迎登入系統");
nameBlock.appendChild(result_Name);
nameBlock.setAttribute("class","mid");
document.getElementById("getName").appendChild(nameBlock);


//處理歷史訊息
// 取得資料
let historyContent=document.getElementById("getHistory").getAttribute("d");
//整理成陣列
historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","").replaceAll("'","")
// console.log(historyContent2);
historyContent3=historyContent2.split(",");
// 取得陣列長度
console.log(historyContent3.length);
// console.log(historyContent3[0]+historyContent3[1]);

if (historyContent3.length!=1){
    let arrayLen=historyContent3.length
    for(let i =0;i<arrayLen/3;i++){
        let historyBlock = document.createElement("div");     //创建一个div元素
        let result_history=document.createTextNode(historyContent3[1+3*i]+" : "+historyContent3[2+3*i]);
        historyBlock.appendChild(result_history);
        historyBlock.setAttribute("class","mid");
        document.getElementById("getHistory").appendChild(historyBlock);    
    }
}



// let historyContent=document.getElementById("getHistory").getAttribute("d");
//整理資料作轉態
// historyContent=historyContent.replaceAll("(","").replaceAll(")","").replaceAll('[','"').replaceAll(']','"')
// historyContent=JSON.parse(historyContent)
// console.log(historyContent[1]);
// historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","")
// historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","").replaceAll("'","")
// len=historyContent2.length
// console.log(len);
// console.log(historyContent2.substr(0, len-2));




// let historyBlock = document.createElement("div");     //创建一个div元素
// let result_history=document.createTextNode(historyContent);
// historyBlock.appendChild(result_history);
// historyBlock.setAttribute("class","mid");
// document.getElementById("getHistory").appendChild(historyBlock);





// var data = "0,1,2,3";
// var arr = JSON.parse("[" + data + "]");
// console.log(arr);

// let nameContent=document.getElementById("getName").getAttribute("d");
// let result=document.createTextNode(num**2);
// nameBlock.appendChild(result);
// nameBlock.setAttribute("class","mid");
// document.getElementById("flagEnd").appendChild(nameBlock);
// console.log(num.replaceAll("(","[").replaceAll(")","]"));
// num = num.replaceAll("'",'"')
// ------console.log(JSON.stringify(num))
// let num2=JSON.parse(num);
// console.log(num2["peopleNow"]);

// 事件監聽器
// let button= document.querySelector("#more_message")

// button.addEventListener("click",function(){
//     let node = document.createElement("div");
//     let textnode = document.createTextNode("WaterWaterWaterWater");
//     node.appendChild(textnode);
//     document.getElementById("myList").appendChild(node);

// })

