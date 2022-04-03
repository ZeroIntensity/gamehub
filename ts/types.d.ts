type Optional<T> = T | null;

type Authorization = {
    username: string;
    password: string;
};

type GraphQLError = {
    message: string;
    locations: {
        line: number;
        column: number;
    };
};

type GraphQLResponse<T> = {
    data: Optional<T>;
    errors: Optional<GraphQLError>;
};

type AccountType = "user" | "admin" | "owner" | "developer";

type Variables = { [key: string]: Optional<string> };
