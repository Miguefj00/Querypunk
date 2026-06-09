import ChallengeCard
    from "./ChallengeCard";

interface Props {

    chapter: any;

    challenges: any[];

    progress: any[];

    onBack: () => void;

    onSelectChallenge: (
        challenge: any
    ) => void;
}

export default function ChallengeList({
                                          chapter,
                                          challenges,
                                          progress,
                                          onBack,
                                          onSelectChallenge
                                      }: Props) {

    return (

        <div>

            <div className="chapter-header">

                <button
                    className="back-button"
                    onClick={onBack}
                >
                    ← Volver a capítulos
                </button>

                <h1 className="chapter-title">
                    {chapter.title}
                </h1>

            </div>

            <div className="challenge-grid">

                {challenges.map(challenge => (

                    <ChallengeCard
                        key={challenge.id}
                        challenge={challenge}
                        progress={progress}
                        onClick={() =>
                            onSelectChallenge(challenge)
                        }
                    />

                ))}

            </div>

        </div>

    );
}