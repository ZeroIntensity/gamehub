export class Input {
    readonly element: HTMLInputElement;
    public validators: Array<Validator>;

    constructor(element: HTMLInputElement) {
        this.element = element;
        this.validators = [];
    }

    private displayMsg(message: string, type: "success" | "error"): void {
        const target = this.element.parentNode?.querySelector("small")!;
        target.innerHTML = message;

        let a = type == "success" ? "text-emerald-400" : "text-rose-400";
        let b = type == "success" ? "text-rose-400" : "text-emerald-400";

        target.classList.add(a);
        target.classList.remove(b);
    }

    public error(message: string) {
        this.displayMsg(message, "error");
    }

    public success(message: string) {
        this.displayMsg(message, "success");
    }

    public addValidator(callback: Validator) {
        this.validators.push(callback);
    }

    public data(): string {
        return this.element.value;
    }

    public clear() {
        this.displayMsg("", "error");
    }
}

export class Form {
    readonly element: HTMLFormElement;
    public inputs: Record<string, Input>;
    private submitCallback?: (
        event: SubmitEvent,
        data: Record<string, string>
    ) => void;

    constructor(id: string) {
        this.element = <HTMLFormElement>document.getElementById(id)!;
        this.inputs = {};
        this.submitCallback = () => {};

        Array.from(this.element.elements).forEach(item => {
            this.inputs[item.id] = new Input(<HTMLInputElement>item);
        });

        this.element.addEventListener("submit", (event: SubmitEvent) => {
            event.preventDefault();
            let validated = true;

            Object.keys(this.inputs).forEach(input => {
                const obj = this.inputs[input];

                obj.validators.forEach(callback => {
                    const response = callback(obj.element.value);

                    if (!response.success) {
                        obj.error(response.message!);
                        validated = false;
                    }
                });
            });

            if (!validated) return;

            if (!this.submitCallback) throw new Error("callback is not set");

            const data: Record<string, string> = {};

            Object.keys(this.inputs).forEach(
                key => (data[key] = this.inputs[key].data())
            );

            this.submitCallback(event, data);
        });
    }

    public getInput(name: string): Input {
        if (!this.inputs.hasOwnProperty(name))
            throw new Error(`input "${name}" does not exist`);

        return this.inputs[name];
    }

    public setCallback(
        callback: (event: SubmitEvent, data: Record<string, string>) => void
    ) {
        this.submitCallback = callback;
    }

    // TODO: optimize this section

    private displayMsg(message: string, type: "success" | "error"): void {
        const target = this.element.querySelector("small")!;
        target.innerHTML = message;

        let a = type == "success" ? "text-emerald-400" : "text-rose-400";
        let b = type == "success" ? "text-rose-400" : "text-emerald-400";

        target.classList.add(a);
        target.classList.remove(b);
    }

    public error(message: string) {
        this.displayMsg(message, "error");
    }

    public success(message: string) {
        this.displayMsg(message, "success");
    }

    public clear() {
        Object.keys(this.inputs).forEach(key => {
            this.inputs[key].clear();
        });
        this.displayMsg("", "error");
    }
}
