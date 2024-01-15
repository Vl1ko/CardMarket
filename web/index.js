let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

let item = "";

let container = document.getElementById("container");


let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");
let btn7 = document.getElementById("btn7");


container.addEventListener("click", function() {

    if (tg.MainButton.isVisible) {

        tg.MainButton.hide();

    }

})



btn1.addEventListener("click", function() {

    if (tg.MainButton.isVisible) {

        tg.MainButton.hide();

    } else {

        tg.MainButton.setText("Выбран товар Gift card Apple 500RUB!");

        item = "1";
        tg.MainButton.show();
    }
});

btn2.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 1500RUB!");
        item = "2";
        tg.MainButton.show();
    }
});

btn3.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 2000RUB!");
        item = "3";
        tg.MainButton.show();
    }
});

btn4.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 3000RUB!");
        item = "4";
        tg.MainButton.show();
    }
});

btn5.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 4000RUB!");
        item = "5";
        tg.MainButton.show();
    }
});

btn6.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 5000RUB!");
        item = "6";
        tg.MainButton.show();
    }
});

btn7.addEventListener("click", function() {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Выбран товар Gift card Apple 10000RUB!");
        item = "7";
        tg.MainButton.show();
    }
});


Telegram.WebApp.onEvent("mainButtonClicked", function() {
    tg.sendData(item);
});


let usercard = document.getElementById("usercard");

let p = document.createElement("p");

p.innerText = `${tg.initDataUnsafe.user.first_name}
${tg.initDataUnsafe.user.last_name}`;

usercard.appendChild(p);