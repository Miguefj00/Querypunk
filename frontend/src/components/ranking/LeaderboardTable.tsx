interface Props {

    entries: any[];
}

export default function LeaderboardTable({
                                             entries
                                         }: Props) {

    return (

        <table className="leaderboard-table">

            <thead>

            <tr>

                <th>#</th>

                <th>Jugador</th>

                <th>Score</th>

                <th>Runs</th>

            </tr>

            </thead>

            <tbody>

            {
                entries.map(
                    (entry) => (

                        <tr key={entry.user_id}>

                            <td>

                                {
                                    entry.position === 1
                                        ? "🥇"
                                        : entry.position === 2
                                            ? "🥈"
                                            : entry.position === 3
                                                ? "🥉"
                                                : `#${entry.position}`
                                }

                            </td>

                            <td>
                                {entry.username}
                            </td>

                            <td>
                                {entry.score}
                            </td>

                            <td>
                                {entry.runs_count}
                            </td>

                        </tr>

                    )
                )
            }

            </tbody>

        </table>

    );
}