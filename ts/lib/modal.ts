export class Modal {
    readonly element: HTMLElement;

    constructor(id: string) {
        this.element = document.getElementById(id)!;
    }

    private addToClass(className: string) {
        this.element.classList.add(className);
    }

    private removeFromClass(className: string) {
        this.element.classList.remove(className);
    }

    public close() {
        this.addToClass("hidden");
    }

    public open() {
        this.removeFromClass("hidden");
    }
}
