const parseCookie = (str: string) =>
    str
        .split(";")
        .map((v: string) => v.split("="))
        .reduce((acc: Record<string, string>, v: Array<string>) => {
            acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(
                v[1].trim()
            );
            return acc;
        }, {});

const cookies = parseCookie(document.cookie);
export const isAuthenticated = cookies.hasOwnProperty("auth");
export default cookies;
