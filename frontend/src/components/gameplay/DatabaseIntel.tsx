type ColumnMeta = {
    name: string;
    type: string;
    key?: "PK" | "FK";
    references?: string;
};

export const GAME_SCHEMA: Record<string, ColumnMeta[]> = {
    Corporation: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Name", type: "TEXT" },
        { name: "Founded_year", type: "INTEGER" },
        { name: "Ceo_name", type: "TEXT" },
        { name: "Net_worth", type: "REAL" },
        { name: "Influence_level", type: "INTEGER" }
    ],

    Corporation_sector: [
        { name: "Id", type: "INTEGER", key: "PK" },
        {
            name: "Corporation_id",
            type: "INTEGER",
            key: "FK",
            references: "Corporation.Id"
        },
        {
            name: "Sector_id",
            type: "INTEGER",
            key: "FK",
            references: "Sector.Id"
        }
    ],

    Headquarter: [
        { name: "Id", type: "INTEGER", key: "PK" },
        {
            name: "Corporation_id",
            type: "INTEGER",
            key: "FK",
            references: "Corporation.Id"
        },
        {
            name: "District_id",
            type: "INTEGER",
            key: "FK",
            references: "District.Id"
        },
        { name: "Main", type: "BOOLEAN" },
        { name: "Security_lvl", type: "INTEGER" },
        { name: "Employees", type: "INTEGER" }
    ],

    Security_incident: [
        { name: "Id", type: "INTEGER", key: "PK" },
        {
            name: "Headquarter_id",
            type: "INTEGER",
            key: "FK",
            references: "Headquarter.Id"
        },
        { name: "Severity", type: "INTEGER" },
        { name: "Description", type: "TEXT" },
        { name: "Date", type: "DATE" }
    ],

    Data_leak: [
        { name: "Id", type: "INTEGER", key: "PK" },
        {
            name: "Corporation_id",
            type: "INTEGER",
            key: "FK",
            references: "Corporation.Id"
        },
        { name: "Title", type: "TEXT" },
        { name: "Confidentiality_lvl", type: "INTEGER" },
        { name: "Files_number", type: "INTEGER" },
        { name: "Date", type: "DATE" }
    ],

    Personnel: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "First_name", type: "TEXT" },
        { name: "Last_name", type: "TEXT" },
        { name: "Salary", type: "REAL" },
        {
            name: "Corporation_id",
            type: "INTEGER",
            key: "FK",
            references: "Corporation.Id"
        },
        {
            name: "Species_id",
            type: "INTEGER",
            key: "FK",
            references: "Species.Id"
        },
        {
            name: "District_id",
            type: "INTEGER",
            key: "FK",
            references: "District.Id"
        }
    ],

    Implant: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Name", type: "TEXT" },
        { name: "Manufacturer", type: "TEXT" },
        { name: "Legality", type: "BOOLEAN" },
        { name: "Power_consumption", type: "REAL" },
        { name: "Type", type: "TEXT" }
    ],

    Personnel_implant: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Install_date", type: "DATE" },
        {
            name: "Personnel_id",
            type: "INTEGER",
            key: "FK",
            references: "Personnel.Id"
        },
        {
            name: "Implant_id",
            type: "INTEGER",
            key: "FK",
            references: "Implant.Id"
        }
    ],

    District: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Name", type: "TEXT" },
        { name: "Population", type: "INTEGER" },
        { name: "Description", type: "TEXT" },
        { name: "Danger_lvl", type: "INTEGER" }
    ],

    Sector: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Budget", type: "REAL" },
        { name: "Director", type: "TEXT" },
        {
            name: "Sector_type_id",
            type: "INTEGER",
            key: "FK",
            references: "Sector_type.Id"
        }
    ],

    Sector_type: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Name", type: "TEXT" },
        { name: "Description", type: "TEXT" }
    ],

    Species: [
        { name: "Id", type: "INTEGER", key: "PK" },
        { name: "Name", type: "TEXT" },
        { name: "Description", type: "TEXT" }
    ]
};

interface Props {
    schema: Record<string, ColumnMeta[]>;
}

export default function DatabaseIntel({ schema }: Props) {
    return (
        <div className="database-intel">
            <h3>DATABASE INTEL</h3>

            {Object.entries(schema).map(([table, columns]) => (
                <details key={table}>
                    <summary>{table}</summary>

                    <ul>
                        {columns.map((column) => (
                            <li key={column.name}>
                                <div className="column-line">
                                    <span className="column-name">
                                        {column.name}
                                    </span>

                                    <span className="column-type">
                                        {column.type}
                                    </span>

                                    {column.key && (
                                        <span
                                            className={`column-key ${column.key.toLowerCase()}`}
                                        >
                                            {column.key}
                                        </span>
                                    )}
                                </div>

                                {column.references && (
                                    <div className="column-ref">
                                        → {column.references}
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                </details>
            ))}
        </div>
    );
}