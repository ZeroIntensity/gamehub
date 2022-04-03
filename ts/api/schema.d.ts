type Comment = {
    author: string;
    likes: Array<string>;
    content: string;
    epoch: number;
    id: string;
};

type CommentData = {
    id: string;
    name: string;
};

type Game = {
    name: string;
    likes: Array<string>;
    comments: Array<Comment>;
    data: string;
};

type GameInput = {
    name: string;
    data: string;
};

type Post = {
    author: string;
    content: string;
    epoch: number;
    id: string;
};

type User = {
    name: string;
    accountType: AccountType;
};

type UserInput = {
    name: string;
    password: string;
};
