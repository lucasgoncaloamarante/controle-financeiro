export const getUsuarios = async () => {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/usuarios`);
    return await response.json();
};

export const getDespesas = async () => {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/despesas`);
    return await response.json();
};