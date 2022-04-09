import login, { logout } from "./api/wrappers/login";
import { isAuthenticated } from "./cookies";
import handleErrors from "./utils/handleErrors";

export async function logIn(name: string, password: string): Promise<boolean> {
    if (isAuthenticated) throw new Error("already logged in");
    const response = await login(name, password);
    return handleErrors(response, "Invalid username or password.");
}

export async function logOut() {
    if (!isAuthenticated) throw new Error("not logged in");
    const response = await logout();

    return handleErrors(response);
}
