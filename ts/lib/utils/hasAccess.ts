const order: Array<AccountType> = ["user", "admin", "owner", "developer"];

export default (actual: AccountType, needed: AccountType) => {
	if (actual == "user") return false;
	return order.indexOf(actual) >= order.indexOf(needed);
};
