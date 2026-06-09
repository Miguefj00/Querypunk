interface Props {

    columns: string[];

    rows: any[][];
}

export default function QueryResults({
                                         columns,
                                         rows
                                     }: Props) {

    if (
        !columns.length
    ) {
        return null;
    }

    return (

        <table
            className="query-results"
        >

            <thead>

            <tr>

                {columns.map(
                    column => (

                        <th
                            key={column}
                        >
                            {column}
                        </th>

                    )
                )}

            </tr>

            </thead>

            <tbody>

            {rows.map(
                (
                    row,
                    index
                ) => (

                    <tr key={index}>

                        {row.map(
                            (
                                cell,
                                cellIndex
                            ) => (

                                <td
                                    key={
                                        cellIndex
                                    }
                                >
                                    {
                                        String(
                                            cell
                                        )
                                    }
                                </td>

                            )
                        )}

                    </tr>

                )
            )}

            </tbody>

        </table>

    );
}