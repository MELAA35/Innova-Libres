document.addEventListener("DOMContentLoaded",async()=>{
    const bracketDiv=document.getElementById("bracket");

    // Cargar datos del servidor
    const db = await fetch("/api/bracket").then(r=>r.json());

    // ----- Renderizado rápido en 6 columnas (rondas) -----
    const rounds=5; // 32→16→8→4→2→1
    let matchIndex=1;
    for(let r=1;r<=rounds;r++){
        const col=document.createElement("div");
        col.className="col";
        const matches=32/Math.pow(2,r);
        for(let m=0;m<matches;m++){
            const match=db.matches[matchIndex];
            const card=document.createElement("div");
            card.className="match round-"+r+(match.winner?" done":"");
            card.dataset.id=matchIndex;

            const tA=document.createElement("div");
            tA.className="team";
            tA.textContent=match.teamA||"---";
            const tB=document.createElement("div");
            tB.className="team";
            tB.textContent=match.teamB||"---";
            if(match.winner===match.teamA) tA.classList.add("winner");
            if(match.winner===match.teamB) tB.classList.add("winner");
            card.append(tA,tB);

            card.onclick=()=>selectWinner(matchIndex,tA.textContent,tB.textContent);
            if(!match.teamA&&!match.teamB) card.classList.add("vacio");
            col.appendChild(card);
            matchIndex++;
        }
        bracketDiv.appendChild(col);
    }

    async function selectWinner(id,teamA,teamB){
        if(teamA==="---"||teamB==="---") return;
        const winner=prompt(`¿Quién ganó? (A/B)\nA) ${teamA}\nB) ${teamB}`);
        if(!winner) return;
        const choice = winner.toUpperCase()==="A"?teamA:teamB;
        await fetch(`/api/match/${id}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({winner:choice})});
        location.reload();
    }
});