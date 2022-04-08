type Optional<T> = T | null;

type GraphQLError = {
    message: string;
    locations: {
        line: number;
        column: number;
    };
};

type GraphQLResponse<T> = {
    data?: T;
    errors?: Array<GraphQLError>;
};

type AccountType = "user" | "admin" | "owner" | "developer";

type Variables = { [key: string]: Optional<string> };

type GQLHeaders = {
    Accept: string;
    "Content-Type": string;
    Authorization?: string;
};

type APIResponse<T extends object> = Promise<GraphQLResponse<T>>;
