interface Props {

    query: string;

    setQuery: (
        query: string
    ) => void;
}

export default function SQLTerminal({
                                        query,
                                        setQuery
                                    }: Props) {

    return (

        <textarea
            className="sql-terminal"
            value={query}
            onFocus={() => {

                if (
                    query ===
                    `SELECT *
FROM table_name;`
                ) {

                    setQuery("");
                }
            }}
            onChange={(e) =>
                setQuery(e.target.value)
            }
        />

    );
}