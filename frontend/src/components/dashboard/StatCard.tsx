import "../../styles/statcard.css";

interface Props {
    title: string;
    value: number;
    suffix?: string;
}

export default function StatCard({
                                     title,
                                     value,
                                     suffix = ""
                                 }: Props) {

    return (

        <div className="stat-card">

            <span className="stat-title">
                {title}
            </span>

            <span className="stat-value">
                {value}{suffix}
            </span>

        </div>

    );
}