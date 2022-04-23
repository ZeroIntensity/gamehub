const order: Array<AccountType> = ["user", "admin", "owner", "developer"];

export default (actual: AccountType, needed: AccountType) => {
	return order.indexOf(actual) >= order.indexOf(needed);
};
