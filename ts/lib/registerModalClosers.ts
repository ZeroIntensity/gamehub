export default () => {
    const modalClosers = document.querySelectorAll('[data-type="modalclose"]');

    modalClosers.forEach(element => {
        const origin = <HTMLElement>element;
        let parent: HTMLElement = origin;

        for (let i = 0; i < 10; i++) {
            if (parent.getAttribute("data-type") == "modal") break;
            parent = parent.parentElement!;
        }

        origin.onclick = () => {
            parent.classList.add("hidden");
        };
    });
};
