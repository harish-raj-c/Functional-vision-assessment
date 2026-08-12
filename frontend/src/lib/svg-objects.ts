export const svgObjects: Record<string, string> = {
  balloon: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="balloonGrad" cx="30%" cy="30%">
        <stop offset="0%" style="stop-color:white;stop-opacity:0.6"/>
        <stop offset="100%" style="stop-color:currentColor;stop-opacity:1"/>
      </radialGradient>
    </defs>
    <ellipse cx="50" cy="42" rx="32" ry="38" fill="url(#balloonGrad)" stroke="currentColor" stroke-width="1.5"/>
    <ellipse cx="40" cy="32" rx="8" ry="12" fill="white" opacity="0.4"/>
    <line x1="50" y1="80" x2="50" y2="92" stroke="currentColor" stroke-width="2"/>
    <polygon points="50,92 46,88 54,88" fill="currentColor"/>
  </svg>`,
  
  football: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="footballGrad" cx="40%" cy="40%">
        <stop offset="0%" style="stop-color:#fff;stop-opacity:0.3"/>
        <stop offset="100%" style="stop-color:#fff;stop-opacity:0"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="50" r="42" fill="currentColor"/>
    <circle cx="50" cy="50" r="42" fill="url(#footballGrad)"/>
    <path d="M50 8 L65 28 L92 33 L75 53 L80 78 L50 68 L20 78 L25 53 L8 33 L35 28 Z" fill="white" opacity="0.25" stroke="white" stroke-width="1.5"/>
    <ellipse cx="35" cy="35" rx="5" ry="4" fill="white" opacity="0.3"/>
  </svg>`,
  
  basketball: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="basketballGrad" cx="35%" cy="35%">
        <stop offset="0%" style="stop-color:#FF8C42"/>
        <stop offset="100%" style="stop-color:#E65100"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="50" r="42" fill="url(#basketballGrad)"/>
    <path d="M8 50 Q50 50 92 50" stroke="#333" stroke-width="3" fill="none"/>
    <path d="M50 8 Q50 50 50 92" stroke="#333" stroke-width="3" fill="none"/>
    <path d="M18 18 Q50 50 82 18" stroke="#333" stroke-width="2.5" fill="none"/>
    <path d="M18 82 Q50 50 82 82" stroke="#333" stroke-width="2.5" fill="none"/>
    <ellipse cx="35" cy="35" rx="8" ry="6" fill="white" opacity="0.2"/>
  </svg>`,
  
  teddy_bear: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="bearGrad" cx="40%" cy="40%">
        <stop offset="0%" style="stop-color:#A0522D"/>
        <stop offset="100%" style="stop-color:#6B3E26"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="58" r="32" fill="url(#bearGrad)"/>
    <circle cx="28" cy="25" r="16" fill="url(#bearGrad)"/>
    <circle cx="72" cy="25" r="16" fill="url(#bearGrad)"/>
    <circle cx="28" cy="25" r="8" fill="#DEB887"/>
    <circle cx="72" cy="25" r="8" fill="#DEB887"/>
    <circle cx="40" cy="52" r="5" fill="#333"/>
    <circle cx="60" cy="52" r="5" fill="#333"/>
    <circle cx="42" cy="51" r="2" fill="white"/>
    <circle cx="62" cy="51" r="2" fill="white"/>
    <ellipse cx="50" cy="68" rx="10" ry="6" fill="#DEB887"/>
    <ellipse cx="50" cy="70" rx="4" ry="3" fill="#333"/>
    <ellipse cx="35" cy="65" rx="6" ry="4" fill="#DEB887" opacity="0.6"/>
    <ellipse cx="65" cy="65" rx="6" ry="4" fill="#DEB887" opacity="0.6"/>
  </svg>`,
  
  cup: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="cupGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:currentColor;stop-opacity:1"/>
        <stop offset="50%" style="stop-color:currentColor;stop-opacity:0.8"/>
        <stop offset="100%" style="stop-color:currentColor;stop-opacity:1"/>
      </linearGradient>
    </defs>
    <path d="M23 28 L28 82 L72 82 L77 28 Z" fill="url(#cupGrad)" stroke="currentColor" stroke-width="1"/>
    <ellipse cx="50" cy="28" rx="27" ry="5" fill="currentColor" opacity="0.7"/>
    <path d="M77 38 Q95 38 95 55 Q95 72 77 72" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>
    <ellipse cx="50" cy="35" rx="20" ry="3" fill="white" opacity="0.2"/>
  </svg>`,
  
  bottle: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bottleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:currentColor;stop-opacity:0.9"/>
        <stop offset="50%" style="stop-color:currentColor;stop-opacity:0.7"/>
        <stop offset="100%" style="stop-color:currentColor;stop-opacity:0.9"/>
      </linearGradient>
    </defs>
    <rect x="42" y="8" width="16" height="12" rx="3" fill="url(#bottleGrad)" stroke="currentColor" stroke-width="1"/>
    <rect x="44" y="4" width="12" height="6" rx="2" fill="currentColor"/>
    <path d="M33 20 L38 88 L62 88 L67 20 Z" fill="url(#bottleGrad)" stroke="currentColor" stroke-width="1"/>
    <ellipse cx="50" cy="20" rx="17" ry="4" fill="currentColor" opacity="0.6"/>
    <rect x="40" y="35" width="20" height="3" fill="white" opacity="0.2"/>
    <rect x="40" y="50" width="20" height="3" fill="white" opacity="0.2"/>
    <rect x="40" y="65" width="20" height="3" fill="white" opacity="0.2"/>
  </svg>`,
  
  apple: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="appleGrad" cx="35%" cy="35%">
        <stop offset="0%" style="stop-color:#FF6B6B"/>
        <stop offset="100%" style="stop-color:#C0392B"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="58" r="36" fill="url(#appleGrad)"/>
    <ellipse cx="35" cy="45" rx="10" ry="8" fill="white" opacity="0.3"/>
    <path d="M50 22 Q50 8 62 14" stroke="#4CAF50" stroke-width="4" fill="none" stroke-linecap="round"/>
    <ellipse cx="62" cy="14" rx="6" ry="4" fill="#4CAF50"/>
    <ellipse cx="55" cy="18" rx="4" ry="3" fill="#FF6B6B"/>
  </svg>`,
  
  book: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bookGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:currentColor;stop-opacity:1"/>
        <stop offset="100%" style="stop-color:currentColor;stop-opacity:0.7"/>
      </linearGradient>
    </defs>
    <rect x="12" y="18" width="76" height="64" rx="4" fill="url(#bookGrad)" stroke="currentColor" stroke-width="1"/>
    <line x1="50" y1="18" x2="50" y2="82" stroke="#333" stroke-width="2"/>
    <rect x="12" y="18" width="38" height="64" rx="4" fill="currentColor" opacity="0.9"/>
    <line x1="18" y1="28" x2="44" y2="28" stroke="#666" stroke-width="1.5"/>
    <line x1="18" y1="38" x2="44" y2="38" stroke="#666" stroke-width="1.5"/>
    <line x1="18" y1="48" x2="44" y2="48" stroke="#666" stroke-width="1.5"/>
    <line x1="56" y1="28" x2="82" y2="28" stroke="#666" stroke-width="1.5"/>
    <line x1="56" y1="38" x2="82" y2="38" stroke="#666" stroke-width="1.5"/>
    <line x1="56" y1="48" x2="82" y2="48" stroke="#666" stroke-width="1.5"/>
  </svg>`,
  
  chair: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="chairGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:currentColor;stop-opacity:1"/>
        <stop offset="50%" style="stop-color:currentColor;stop-opacity:0.8"/>
        <stop offset="100%" style="stop-color:currentColor;stop-opacity:1"/>
      </linearGradient>
    </defs>
    <rect x="23" y="12" width="54" height="50" rx="5" fill="url(#chairGrad)" stroke="currentColor" stroke-width="1"/>
    <rect x="23" y="58" width="10" height="30" rx="2" fill="url(#chairGrad)" stroke="currentColor" stroke-width="1"/>
    <rect x="67" y="58" width="10" height="30" rx="2" fill="url(#chairGrad)" stroke="currentColor" stroke-width="1"/>
    <rect x="18" y="52" width="64" height="10" rx="3" fill="url(#chairGrad)" stroke="currentColor" stroke-width="1"/>
    <rect x="28" y="18" width="44" height="38" rx="3" fill="currentColor" opacity="0.2"/>
  </svg>`,
  
  clock: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="clockGrad" cx="50%" cy="50%">
        <stop offset="0%" style="stop-color:#fff"/>
        <stop offset="100%" style="stop-color:#f0f0f0"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="50" r="44" fill="url(#clockGrad)" stroke="#333" stroke-width="4"/>
    <circle cx="50" cy="50" r="40" fill="none" stroke="#ddd" stroke-width="1"/>
    <line x1="50" y1="50" x2="50" y2="18" stroke="#333" stroke-width="4" stroke-linecap="round"/>
    <line x1="50" y1="50" x2="75" y2="50" stroke="#333" stroke-width="3" stroke-linecap="round"/>
    <circle cx="50" cy="50" r="5" fill="#333"/>
    <circle cx="50" cy="12" r="2" fill="#333"/>
    <circle cx="88" cy="50" r="2" fill="#333"/>
    <circle cx="50" cy="88" r="2" fill="#333"/>
    <circle cx="12" cy="50" r="2" fill="#333"/>
  </svg>`,
  
  flower: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="flowerGrad" cx="50%" cy="50%">
        <stop offset="0%" style="stop-color:#FFB6C1"/>
        <stop offset="100%" style="stop-color:#FF69B4"/>
      </radialGradient>
    </defs>
    <circle cx="50" cy="35" r="14" fill="url(#flowerGrad)"/>
    <circle cx="35" cy="50" r="14" fill="url(#flowerGrad)"/>
    <circle cx="65" cy="50" r="14" fill="url(#flowerGrad)"/>
    <circle cx="40" cy="68" r="14" fill="url(#flowerGrad)"/>
    <circle cx="60" cy="68" r="14" fill="url(#flowerGrad)"/>
    <circle cx="50" cy="52" r="12" fill="#FFD700"/>
    <circle cx="50" cy="52" r="8" fill="#FFA500"/>
    <line x1="50" y1="64" x2="50" y2="95" stroke="#228B22" stroke-width="5" stroke-linecap="round"/>
    <path d="M50 75 Q35 70 30 80" stroke="#228B22" stroke-width="3" fill="none"/>
    <path d="M50 82 Q65 77 70 87" stroke="#228B22" stroke-width="3" fill="none"/>
  </svg>`,
  
  toy_car: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="carGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:#5DADE2"/>
        <stop offset="100%" style="stop-color:#2E86C1"/>
      </linearGradient>
    </defs>
    <rect x="12" y="38" width="76" height="28" rx="8" fill="url(#carGrad)" stroke="#21618C" stroke-width="1"/>
    <rect x="55" y="22" width="28" height="22" rx="6" fill="url(#carGrad)" stroke="#21618C" stroke-width="1"/>
    <rect x="60" y="26" width="18" height="14" rx="3" fill="#85C1E9"/>
    <circle cx="28" cy="72" r="12" fill="#333"/>
    <circle cx="28" cy="72" r="8" fill="#666"/>
    <circle cx="72" cy="72" r="12" fill="#333"/>
    <circle cx="72" cy="72" r="8" fill="#666"/>
    <rect x="18" y="42" width="15" height="10" rx="2" fill="#85C1E9" opacity="0.8"/>
  </svg>`,
  
  dog: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="dogGrad" cx="40%" cy="40%">
        <stop offset="0%" style="stop-color:#A0826D"/>
        <stop offset="100%" style="stop-color:#6B4423"/>
      </radialGradient>
    </defs>
    <ellipse cx="50" cy="62" rx="32" ry="28" fill="url(#dogGrad)"/>
    <circle cx="50" cy="40" r="22" fill="url(#dogGrad)"/>
    <polygon points="28,22 22,2 40,18" fill="url(#dogGrad)"/>
    <polygon points="72,22 78,2 60,18" fill="url(#dogGrad)"/>
    <ellipse cx="28" cy="22" rx="10" ry="8" fill="#DEB887"/>
    <ellipse cx="72" cy="22" rx="10" ry="8" fill="#DEB887"/>
    <circle cx="40" cy="38" r="5" fill="#333"/>
    <circle cx="60" cy="38" r="5" fill="#333"/>
    <circle cx="42" cy="37" r="2" fill="white"/>
    <circle cx="62" cy="37" r="2" fill="white"/>
    <ellipse cx="50" cy="50" rx="10" ry="6" fill="#DEB887"/>
    <ellipse cx="50" cy="52" rx="4" ry="3" fill="#333"/>
    <ellipse cx="35" cy="68" rx="8" ry="5" fill="#DEB887" opacity="0.7"/>
    <ellipse cx="65" cy="68" rx="8" ry="5" fill="#DEB887" opacity="0.7"/>
  </svg>`,
  
  cat: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="catGrad" cx="40%" cy="40%">
        <stop offset="0%" style="stop-color:#FFB347"/>
        <stop offset="100%" style="stop-color:#CC7A00"/>
      </radialGradient>
    </defs>
    <ellipse cx="50" cy="62" rx="28" ry="32" fill="url(#catGrad)"/>
    <circle cx="50" cy="35" r="20" fill="url(#catGrad)"/>
    <polygon points="32,18 26,0 45,16" fill="url(#catGrad)"/>
    <polygon points="68,18 74,0 55,16" fill="url(#catGrad)"/>
    <polygon points="32,18 28,8 42,16" fill="#DEB887"/>
    <polygon points="68,18 72,8 58,16" fill="#DEB887"/>
    <circle cx="42" cy="33" r="5" fill="#333"/>
    <circle cx="58" cy="33" r="5" fill="#333"/>
    <circle cx="44" cy="32" r="2" fill="white"/>
    <circle cx="60" cy="32" r="2" fill="white"/>
    <ellipse cx="50" cy="48" rx="8" ry="5" fill="#FFB6C1"/>
    <ellipse cx="50" cy="50" rx="3" ry="2" fill="#FF69B4"/>
    <line x1="35" y1="42" x2="38" y2="45" stroke="#333" stroke-width="1"/>
    <line x1="65" y1="42" x2="62" y2="45" stroke="#333" stroke-width="1"/>
  </svg>`,
  
  gift_box: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="giftGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#E74C3C"/>
        <stop offset="100%" style="stop-color:#C0392B"/>
      </linearGradient>
      <linearGradient id="ribbonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#F1C40F"/>
        <stop offset="50%" style="stop-color:#F39C12"/>
        <stop offset="100%" style="stop-color:#F1C40F"/>
      </linearGradient>
    </defs>
    <rect x="13" y="28" width="74" height="58" rx="3" fill="url(#giftGrad)" stroke="#922B21" stroke-width="1"/>
    <rect x="46" y="28" width="8" height="58" fill="url(#ribbonGrad)" stroke="#B7950B" stroke-width="1"/>
    <rect x="13" y="48" width="74" height="8" fill="url(#ribbonGrad)" stroke="#B7950B" stroke-width="1"/>
    <path d="M50 28 Q50 12 68 18 Q50 24 50 28" fill="url(#ribbonGrad)" stroke="#B7950B" stroke-width="1"/>
    <path d="M50 28 Q50 12 32 18 Q50 24 50 28" fill="url(#ribbonGrad)" stroke="#B7950B" stroke-width="1"/>
    <ellipse cx="50" cy="18" rx="12" ry="8" fill="url(#ribbonGrad)" stroke="#B7950B" stroke-width="1"/>
    <rect x="18" y="33" width="24" height="10" fill="white" opacity="0.15"/>
    <rect x="58" y="33" width="24" height="10" fill="white" opacity="0.15"/>
  </svg>`,
  
  plant: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="potGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#8B4513"/>
        <stop offset="50%" style="stop-color:#A0522D"/>
        <stop offset="100%" style="stop-color:#8B4513"/>
      </linearGradient>
      <radialGradient id="leafGrad" cx="30%" cy="30%">
        <stop offset="0%" style="stop-color:#4CAF50"/>
        <stop offset="100%" style="stop-color:#2E7D32"/>
      </radialGradient>
    </defs>
    <rect x="38" y="58" width="24" height="38" rx="4" fill="url(#potGrad)" stroke="#5D3A1A" stroke-width="1"/>
    <ellipse cx="50" cy="58" rx="12" ry="4" fill="#6B3E26"/>
    <ellipse cx="50" cy="32" rx="28" ry="32" fill="url(#leafGrad)"/>
    <ellipse cx="28" cy="45" rx="18" ry="24" fill="url(#leafGrad)"/>
    <ellipse cx="72" cy="45" rx="18" ry="24" fill="url(#leafGrad)"/>
    <ellipse cx="50" cy="25" rx="15" ry="18" fill="#66BB6A"/>
    <ellipse cx="35" cy="38" rx="10" ry="14" fill="#66BB6A"/>
    <ellipse cx="65" cy="38" rx="10" ry="14" fill="#66BB6A"/>
    <path d="M50 32 Q40 25 35 30" stroke="#1B5E20" stroke-width="1" fill="none"/>
    <path d="M50 32 Q60 25 65 30" stroke="#1B5E20" stroke-width="1" fill="none"/>
  </svg>`
};

export function getObjectSVG(type: string, color?: string): string {
  let svg = svgObjects[type] || svgObjects.balloon;
  if (color) {
    svg = svg.replace(/fill="[^"]*"/g, `fill="${color}"`);
  }
  return svg;
}
