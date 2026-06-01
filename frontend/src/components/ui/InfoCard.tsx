import "../../styles/infocard.css";

interface Props {

    title: string;

    children: React.ReactNode;
}

export default function InfoCard({
                                     title,
                                     children,
                                 }: Props) {

    return (

        <div className="info-card cyberpunk-panel">

            <h3 className="cyberpunk-title">
                {title}
            </h3>

            <div className="info-card-content">
                {children}
            </div>

        </div>
    );
}