function ListaEmpresas({ empresas, onEdit, onDelete }) {
    if (empresas.length === 0) {
        return <p className="text-center text-gray-500 mt-8">Nenhuma empresa encontrada.</p>;
    }

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg shadow">
                <thead className="bg-gray-100">
                    <tr>
                        <th className="th-cell">Nome</th>
                        <th className="th-cell">Cidade</th>
                        <th className="th-cell">Ramo</th>
                        <th className="th-cell">Email</th>
                        <th className="th-cell">Ações</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {empresas.map((empresa) => (
                        <tr key={empresa.id} className="hover:bg-gray-50">
                            <td className="td-cell font-medium text-gray-900">{empresa.nome}</td>
                            <td className="td-cell text-gray-600">{empresa.cidade}</td>
                            <td className="td-cell text-gray-600">{empresa.ramo_atuacao}</td>
                            <td className="td-cell text-gray-600">{empresa.email_contato}</td>
                            <td className="td-cell space-x-2">
                                <button onClick={() => onEdit(empresa)} className="text-indigo-600 hover:text-indigo-900 font-medium">Editar</button>
                                <button onClick={() => onDelete(empresa.id)} className="text-red-600 hover:text-red-900 font-medium">Excluir</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ListaEmpresas;