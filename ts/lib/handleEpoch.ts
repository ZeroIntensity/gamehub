export default () => {
    const elements = document.querySelectorAll('[data-type="epoch"]');

    elements.forEach(element => {
        const epoch = Number(element.innerHTML);
        if (isNaN(epoch)) return;

        const date = new Date(epoch * 1000);
        const month = date.toLocaleString("default", { month: "long" });

        (element as HTMLElement).style.display = "block";
        element.innerHTML = `${month} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
    });
};
