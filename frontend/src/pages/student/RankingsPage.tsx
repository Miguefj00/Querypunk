import { useEffect, useState } from "react";

import {
    getChapters
} from "../../services/chapters.service";

import {
    getChallenges
} from "../../services/challenges.service";

import {
    getChapterLeaderboard,
    getGlobalLeaderboard
} from "../../services/rankings.service";

import {
    getChallengeLeaderboard
} from "../../services/rankings.service";


import {
    getGameSettings
} from "../../services/settings.service";

import LeaderboardTable
    from "../../components/LeaderboardTable.tsx";

import "../../styles/rankings.css"

export default function StudentRankingsPage() {

    const [entries, setEntries] =
        useState([]);

    const [settings, setSettings] =
        useState<any>(null);

    const [loading, setLoading] =
        useState(true);

    const [activeTab, setActiveTab] =
        useState("global");

    const [chapters, setChapters] =
        useState([]);

    const [selectedChapter,
        setSelectedChapter] =
        useState<number | null>(null);

    const [chapterLeaderboard,
        setChapterLeaderboard] =
        useState([]);

    const [chapterLoading,
        setChapterLoading] =
        useState(false);

    const [challenges, setChallenges] =
        useState([]);

    const [selectedChallenge,
        setSelectedChallenge] =
        useState<number | null>(null);

    const [challengeLeaderboard,
        setChallengeLeaderboard] =
        useState([]);

    const [challengeLoading,
        setChallengeLoading] =
        useState(false);

    useEffect(() => {

        loadData();

    }, []);

    useEffect(() => {

        if (
            activeTab !== "chapter" ||
            !selectedChapter
        ) {
            return;
        }

        loadChapterLeaderboard();

    }, [activeTab, selectedChapter]);

    useEffect(() => {

        if (
            activeTab !== "global" ||
            !settings?.show_global_leaderboard
        ) {
            return;
        }

        loadGlobalLeaderboard();

    }, [activeTab, settings]);

    useEffect(() => {

        if (!selectedChapter) return;

        loadChallenges();

    }, [selectedChapter]);

    useEffect(() => {

        if (
            activeTab !== "challenge" ||
            !selectedChallenge
        ) {
            return;
        }

        loadChallengeLeaderboard();

    }, [activeTab, selectedChallenge]);

    const loadGlobalLeaderboard = async () => {

        try {

            const data =
                await getGlobalLeaderboard();

            setEntries(data);

        } catch (error) {

            console.error(error);
        }
    };

    const loadChapterLeaderboard =
        async () => {

            try {

                setChapterLoading(true);

                const data =
                    await getChapterLeaderboard(
                        selectedChapter!
                    );

                setChapterLeaderboard(data);

            } catch (error) {

                console.error(error);

            } finally {

                setChapterLoading(false);
            }
        };

    const loadChallenges = async () => {

        try {

            const data =
                await getChallenges(
                    selectedChapter!
                );

            setChallenges(data);

            if (data.length > 0) {

                setSelectedChallenge(
                    data[0].id
                );
            }

        } catch (error) {

            console.error(error);
        }
    };
    const loadChallengeLeaderboard =
        async () => {

            try {

                setChallengeLoading(true);

                const data =
                    await getChallengeLeaderboard(
                        selectedChallenge!
                    );

                setChallengeLeaderboard(data);

            } catch (error) {

                console.error(error);

            } finally {

                setChallengeLoading(false);
            }
        };


    const loadData = async () => {

        try {

            const [
                gameSettings,
                chapterData
            ] = await Promise.all([
                getGameSettings(),
                getChapters()
            ]);

            setSettings(gameSettings);

            setChapters(chapterData);

            if (chapterData.length > 0) {

                setSelectedChapter(
                    chapterData[0].id
                );
            }

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);
        }
    };

    if (loading) {

        return (

            <div>

                Cargando rankings...

            </div>

        );
    }

    return (

        <div className="rankings-page">

            <div className="leaderboard-tabs">

                <button
                    className={
                        activeTab === "global"
                            ? "active"
                            : ""
                    }
                    onClick={() =>
                        setActiveTab("global")
                    }
                >
                    Global
                </button>

                <button
                    className={
                        activeTab === "chapter"
                            ? "active"
                            : ""
                    }
                    onClick={() =>
                        setActiveTab("chapter")
                    }
                >
                    Capítulos
                </button>

                <button
                    className={
                        activeTab === "challenge"
                            ? "active"
                            : ""
                    }
                    onClick={() =>
                        setActiveTab("challenge")
                    }
                >
                    Retos
                </button>

            </div>

            {/* GLOBAL */}

            {
                activeTab === "global" && (

                    settings?.show_global_leaderboard
                        ? (

                            <LeaderboardTable
                                entries={entries}
                            />

                        ) : (

                            <div className="ranking-disabled">

                                Ranking global oculto por el profesor

                            </div>

                        )

                )
            }

            {/* CHAPTER */}

            {
                activeTab === "chapter" && (

                    settings?.show_chapter_leaderboard
                        ? (

                            <>

                                <div className="ranking-filters">

                                    <div>

                                        <div className="ranking-filter-label">

                                            CAPÍTULO

                                        </div>

                                        <select
                                            className="ranking-select"
                                            value={selectedChapter ?? ""}
                                            onChange={(e) =>
                                                setSelectedChapter(
                                                    Number(
                                                        e.target.value
                                                    )
                                                )
                                            }
                                        >

                                            {
                                                chapters.map(
                                                    (chapter: any) => (

                                                        <option
                                                            key={chapter.id}
                                                            value={chapter.id}
                                                        >
                                                            {chapter.title}
                                                        </option>

                                                    )
                                                )
                                            }

                                        </select>

                                    </div>

                                </div>

                                {
                                    chapterLoading ? (

                                        <div>

                                            Cargando ranking...

                                        </div>

                                    ) : (

                                        <LeaderboardTable
                                            entries={
                                                chapterLeaderboard
                                            }
                                        />

                                    )
                                }

                            </>

                        ) : (

                            <div className="ranking-disabled">

                                Ranking por capítulo oculto por el profesor

                            </div>

                        )

                )
            }

            {/* CHALLENGE */}

            {
                activeTab === "challenge" && (

                    settings?.show_challenge_leaderboard
                        ? (

                            <>

                                <div className="ranking-filters">

                                    <div>

                                        <div className="ranking-filter-label">

                                            CAPÍTULO

                                        </div>

                                        <select
                                            className="ranking-select"
                                            value={selectedChapter ?? ""}
                                            onChange={(e) =>
                                                setSelectedChapter(
                                                    Number(
                                                        e.target.value
                                                    )
                                                )
                                            }
                                        >

                                            {
                                                chapters.map(
                                                    (chapter: any) => (

                                                        <option
                                                            key={chapter.id}
                                                            value={chapter.id}
                                                        >
                                                            {chapter.title}
                                                        </option>

                                                    )
                                                )
                                            }

                                        </select>

                                    </div>

                                    <div>

                                        <div className="ranking-filter-label">

                                            RETO

                                        </div>

                                        <select
                                            className="ranking-select"
                                            value={
                                                selectedChallenge ?? ""
                                            }
                                            onChange={(e) =>
                                                setSelectedChallenge(
                                                    Number(
                                                        e.target.value
                                                    )
                                                )
                                            }
                                        >

                                            {
                                                challenges.map(
                                                    (challenge: any) => (

                                                        <option
                                                            key={challenge.id}
                                                            value={challenge.id}
                                                        >
                                                            {challenge.title}
                                                        </option>

                                                    )
                                                )
                                            }

                                        </select>

                                    </div>

                                </div>

                                {
                                    challengeLoading ? (

                                        <div>

                                            Cargando ranking...

                                        </div>

                                    ) : (

                                        <LeaderboardTable
                                            entries={
                                                challengeLeaderboard
                                            }
                                        />

                                    )
                                }

                            </>

                        ) : (

                            <div className="ranking-disabled">

                                Ranking por reto oculto por el profesor

                            </div>

                        )

                )
            }

        </div>

    );
}