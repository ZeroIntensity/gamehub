const elements = document.querySelectorAll('[data-type="epoch"]');

elements.forEach(element => {
    const epoch = Number(element.innerHTML);
    const date = new Date(epoch * 1000);
    const month = date.toLocaleString("default", { month: "long" });

    element.innerHTML = `${month} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
});
