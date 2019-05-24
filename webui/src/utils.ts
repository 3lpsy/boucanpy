export const capitalize = (val: string): string => {
    if (val) {
        return val.charAt(0).toUpperCase() + val.slice(1);
    }
    return val;
};
