export type CommentSchema = {
	author: string;
	content: string;
	epoch: number;
	id: string;
	accountType: AccountType;
};

export type CommentDataSchema = {
	id: string;
	name: string;
};

export type GameSchema = {
	name: string;
	likes: Array<string>;
	comments: Array<Comment>;
	data: string;
};

export type GameInputSchema = {
	name: string;
	data: string;
};

export type PostSchema = {
	author: string;
	content: string;
	epoch: number;
	id: string;
	title: string;
};

export type UserSchema = {
	name: string;
	accountType: AccountType;
};

export type UserInputSchema = {
	name: string;
	password: string;
};

export type Comment = Partial<CommentSchema>;

export type CommentData = Partial<CommentDataSchema>;

export type Game = Partial<GameSchema>;

export type Post = Partial<PostSchema>;

export type User = Partial<UserSchema>;
