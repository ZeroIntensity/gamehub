export default (text: string, pattern: RegExp) => {
    return !!text.search(pattern);
};
