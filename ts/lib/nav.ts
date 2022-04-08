export default () => {
    const elements = document.querySelectorAll('[data-type="navlink"]');

    elements.forEach((element: Element) => {
        if ((element as HTMLAnchorElement).href == window.location.href) {
            element.classList.add("bg-zinc-700");
        }
    });
};
