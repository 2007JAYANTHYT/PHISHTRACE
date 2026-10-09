import React, { useEffect, useRef } from 'react';
import { MapPin, Globe, AlertTriangle, ShieldCheck, Server } from 'lucide-react';
import { HopInfo } from '../../lib/types';
import L from 'leaflet';

interface HopMapProps {
  hops: HopInfo[];
  candidateIp?: string;
  originCaveat?: string;
}

export const HopMap: React.FC<HopMapProps> = ({
  hops,
  candidateIp,
  originCaveat
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  // Extract hops with valid coordinates
  const geoHops = hops.filter(
    (h) => h.geo && h.geo.latitude !== undefined && h.geo.longitude !== undefined && !h.is_private
  );

  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Clean previous map instance if re-rendering
    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    if (geoHops.length === 0) return;

    try {
      // Default center around first geo hop or world center
      const firstLat = geoHops[0].geo!.latitude || 20;
      const firstLng = geoHops[0].geo!.longitude || 0;

      const map = L.map(mapContainerRef.current, {
        center: [firstLat, firstLng],
        zoom: 3,
        zoomControl: true,
        attributionControl: false,
      });

      // Dark style OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
      }).addTo(map);

      const latlngs: [number, number][] = [];

      // Add pins for each hop
      geoHops.forEach((hop) => {
        const lat = hop.geo!.latitude!;
        const lng = hop.geo!.longitude!;
        latlngs.push([lat, lng]);

        const isOrigin = hop.ip === candidateIp || hop.hop_number === 1;

        const iconHtml = `
          <div style="
            background-color: ${isOrigin ? '#ef4444' : '#06b6d4'};
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 2px solid #ffffff;
            box-shadow: 0 0 10px ${isOrigin ? '#ef4444' : '#06b6d4'};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 11px;
            color: #ffffff;
          ">
            ${hop.hop_number}
          </div>
        `;

        const customIcon = L.divIcon({
          html: iconHtml,
          className: 'hop-marker',
          iconSize: [24, 24],
          iconAnchor: [12, 12],
        });

        const marker = L.marker([lat, lng], { icon: customIcon }).addTo(map);
        marker.bindPopup(`
          <div style="font-family:sans-serif;font-size:12px;color:#0f172a;line-height:1.4;">
            <strong>Hop #${hop.hop_number} ${isOrigin ? '(Candidate Origin)' : ''}</strong><br/>
            IP: <code>${hop.ip}</code><br/>
            Location: ${hop.geo!.city}, ${hop.geo!.country}<br/>
            Organization: ${hop.geo!.org || 'Unknown'}<br/>
            Confidence: ${Math.round(hop.confidence * 100)}%
          </div>
        `);
      });

      // Draw dashed trajectory connecting hops
      if (latlngs.length > 1) {
        L.polyline(latlngs, {
          color: '#38bdf8',
          weight: 2,
          opacity: 0.8,
          dashArray: '6, 8',
        }).addTo(map);
      }

      mapInstanceRef.current = map;
    } catch (e) {
      console.warn("Leaflet initialization fallback:", e);
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [hops, candidateIp]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Globe className="h-5 w-5 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
            Received Relay Trace & Geo-Intelligence
          </h3>
        </div>
        <span className="text-[11px] font-mono text-slate-400">
          {hops.length} Total Hops | {geoHops.length} Geolocated Public MTAs
        </span>
      </div>

      {/* Map display */}
      <div className="relative h-64 w-full rounded-lg overflow-hidden border border-slate-800 bg-slate-950 mb-4">
        {geoHops.length > 0 ? (
          <div ref={mapContainerRef} className="w-full h-full" />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 text-xs">
            <Server className="h-8 w-8 mb-2 text-slate-600" />
            <p>All recorded hops reside in private intranet subnets (RFC1918) or lack public client IPs.</p>
          </div>
        )}
      </div>

      {/* Attribution Caveat Callout */}
      {originCaveat && (
        <div className="p-3 rounded-lg bg-amber-950/40 border border-amber-800/60 mb-4 text-xs text-amber-200/90 flex items-start gap-2.5">
          <AlertTriangle className="h-4 w-4 shrink-0 text-amber-400 mt-0.5" />
          <div className="leading-relaxed">
            <span className="font-semibold text-amber-300">Origin Attribution Caveat: </span>
            {originCaveat}
          </div>
        </div>
      )}

      {/* Hop by Hop Timeline */}
      <div className="space-y-2 mt-4">
        <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
          Hop-by-Hop Transmission Chain (Chronological)
        </h4>
        {hops.map((h) => {
          const isCandidate = h.ip === candidateIp;
          return (
            <div
              key={h.hop_number}
              className={`p-2.5 rounded-lg border text-xs flex flex-col md:flex-row md:items-center justify-between gap-2 ${
                isCandidate
                  ? 'bg-red-950/30 border-red-800/80 text-red-200'
                  : h.is_private
                  ? 'bg-slate-950/40 border-slate-800/60 text-slate-400'
                  : 'bg-slate-900 border-slate-800 text-slate-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <span
                  className={`w-6 h-6 rounded-full flex items-center justify-center font-mono font-bold text-[10px] ${
                    isCandidate
                      ? 'bg-red-500 text-white'
                      : h.is_private
                      ? 'bg-slate-800 text-slate-400'
                      : 'bg-cyan-600 text-slate-950'
                  }`}
                >
                  #{h.hop_number}
                </span>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-slate-100">{h.ip || 'No IP Captured'}</span>
                    {isCandidate && (
                      <span className="px-1.5 py-0.2 rounded bg-red-900 text-red-200 text-[9px] font-semibold uppercase">
                        Candidate Origin
                      </span>
                    )}
                    {h.is_private && (
                      <span className="px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 text-[9px] font-mono">
                        RFC1918 Private
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-slate-400">
                    From: <span className="font-mono text-slate-300">{h.from_host}</span> by <span className="font-mono text-slate-300">{h.by_host}</span>
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-4 text-right text-[11px]">
                {h.geo && !h.is_private ? (
                  <div>
                    <p className="font-medium text-slate-200">{h.geo.city}, {h.geo.country}</p>
                    <p className="text-[10px] text-slate-400">{h.geo.org}</p>
                  </div>
                ) : (
                  <span className="text-slate-500 italic">{h.uncertainty_reason || 'Internal MTA'}</span>
                )}
                <div className="text-right">
                  <span className="text-[10px] font-mono text-slate-400 block">Confidence</span>
                  <span className="font-mono font-bold text-cyan-400">{Math.round(h.confidence * 100)}%</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
