import { useEffect, useState } from "react";

import ChapterList
    from "../../components/gameplay/ChapterList.tsx";

import ChallengeList
    from "../../components/gameplay/ChallengeList.tsx";

import "../../styles/challenge.css";

import {
    getChapters
} from "../../services/chapters.service.ts";

import {
    getMyChallengesProgress
} from "../../services/progress.service.ts";

import ChallengeModal
    from "../../components/gameplay/ChallengeModal.tsx";

import "../../styles/gameplay.css"
import {getChallenges} from "../../services/challenges.service.ts";

import type {
    Chapter,
    SolvedChallenge
} from "../../types/gameplay.types.ts";

export default function GameplayPage() {

    const [chapters, setChapters] =
        useState<Chapter[]>([]);

    const [progress, setProgress] =
        useState<SolvedChallenge[]>([]);

    const [selectedChapter, setSelectedChapter] =
        useState<Chapter | null>(null);

    const [chapterTotals,
        setChapterTotals] =
        useState<Record<number, number>>(
            {}
        );

    const [challenges, setChallenges] =
        useState<any[]>([]);

    const [selectedChallenge,
        setSelectedChallenge] =
        useState<any | null>(null);

    const handleSelectChapter =
        async (chapter: Chapter) => {

            try {

                const data =
                    await getChallenges(
                        chapter.id
                    );

                setChallenges(data);

                setSelectedChapter(
                    chapter
                );

            } catch (error) {

                console.error(error);
            }
        };

    const refreshProgress = async () => {

        const progressData =
            await getMyChallengesProgress();

        setProgress(progressData);
    };

    useEffect(() => {

        async function loadData() {

            try {

                const chaptersData =
                    await getChapters();

                const progressData =
                    await getMyChallengesProgress();

                const totalsByChapter:
                    Record<number, number> = {};

                for (const chapter of chaptersData) {

                    const chapterChallenges =
                        await getChallenges(
                            chapter.id
                        );

                    totalsByChapter[
                        chapter.id
                        ] =
                        chapterChallenges.length;
                }

                setChapterTotals(
                    totalsByChapter
                );

                setChapters(
                    chaptersData
                );

                setProgress(
                    progressData
                );

            } catch (error) {

                console.error(error);
            }
        }

        loadData();

    }, []);

    return (

        <div className="gameplay-page">

            {
                !selectedChapter
                    ? (

                        <ChapterList
                            chapters={chapters}
                            progress={progress}
                            chapterTotals={chapterTotals}
                            onSelect={handleSelectChapter}
                        />

                    )
                    : (

                        <ChallengeList
                            chapter={selectedChapter}
                            challenges={challenges}
                            progress={progress}
                            onSelectChallenge={
                                setSelectedChallenge
                            }
                            onBack={() => {

                                setSelectedChapter(
                                    null
                                );

                                setChallenges([]);
                            }}
                        />

                    )
            }

            {
                selectedChallenge && (

                    <ChallengeModal
                        challenge={selectedChallenge}
                        onClose={() =>
                            setSelectedChallenge(null)
                        }
                        onChallengeSolved={refreshProgress}
                    />

                )
            }

        </div>
    );
}