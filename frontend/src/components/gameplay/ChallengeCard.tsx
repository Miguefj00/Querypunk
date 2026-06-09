interface Props {

    challenge: any;

    progress: any[];

    onClick: () => void;
}

export default function ChallengeCard({
                                          challenge,
                                          progress,
                                          onClick
                                      }: Props) {

    const solved =
        progress.find(
            p =>
                p.challenge_id ===
                challenge.id
        );

    return (

        <div
            className="challenge-card"
            onClick={onClick}
        >

            <div className="challenge-card-content">

                <h3>
                    {challenge.title}
                </h3>

            </div>

            <div className="challenge-card-footer">

                <div className="challenge-difficulty">
                    {challenge.difficulty}
                </div>

                <div
                    className={
                        solved
                            ? "challenge-solved"
                            : "challenge-pending"
                    }
                >
                    {
                        solved
                            ? "✓ Resuelto"
                            : "Pendiente"
                    }
                </div>

            </div>

        </div>

    );
}