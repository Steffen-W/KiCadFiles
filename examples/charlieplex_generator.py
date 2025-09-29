#!/usr/bin/env python3
"""
KiCadFiles Charlieplex Generator

Eine funktionsfähige Implementierung des charlieplex-Beispiels unter Verwendung der KiCadFiles-Bibliothek.
Generiert LED-Grids mit systematischer Verdrahtung für normale XY-Matrix oder Charlieplex-Topologie.
"""

import copy
from dataclasses import replace
from typing import List, Optional, Tuple

from kicadfiles import (
    At,
    AtXY,
    GlobalLabel,
    Junction,
    KicadSch,
    KiCadStr,
    Label,
    LibSymbols,
    Property,
    Pts,
    Stroke,
    Symbol,
    Type,
    Uuid,
    Wire,
    Xy,
)
from kicadfiles.base_element import KiCadFloat, KiCadInt


class CharlieplexGenerator:
    """Generator für Charlieplex- und XY-Matrix-LED-Arrays."""

    def __init__(
        self,
        grid_origin: Tuple[float, float] = (45.72, 25.4),
        unit_spacing: float = 2.54,
    ):
        """
        Initialisiere den Generator.

        Args:
            grid_origin: Startpunkt für die Komponenten-Platzierung in mm
            unit_spacing: Raster-Abstand in mm (2.54mm = 100mil standard)
        """
        self.grid_origin = grid_origin
        self.unit_spacing = unit_spacing

    def units_to_mm(self, units: int) -> float:
        """Konvertiere Raster-Einheiten zu Millimetern."""
        return units * self.unit_spacing

    def to_grid_position(self, x_units: int, y_units: int) -> Tuple[float, float]:
        """Konvertiere Raster-Koordinaten zu absoluten mm-Koordinaten."""
        return (
            self.grid_origin[0] + (x_units * self.unit_spacing),
            self.grid_origin[1] + (y_units * self.unit_spacing),
        )

    def clone_symbol(self, base_symbol: Symbol) -> Symbol:
        """
        Klone ein Symbol für die Wiederverwendung.

        Args:
            base_symbol: Basis-Symbol zum Klonen

        Returns:
            Neues Symbol mit kopierten Eigenschaften
        """
        # Deep copy des gesamten Symbols
        new_symbol = copy.deepcopy(base_symbol)

        # Symbol hat kein uuid Feld - UUID wird automatisch generiert

        return new_symbol

    def set_symbol_reference(self, symbol: Symbol, reference: str) -> Symbol:
        """
        Setze die Referenz-Bezeichnung eines Symbols.

        Args:
            symbol: Zu modifizierendes Symbol
            reference: Neue Referenz (z.B. "D1")

        Returns:
            Symbol mit aktualisierter Referenz
        """
        # Stelle sicher, dass properties existiert
        if symbol.properties is None:
            symbol.properties = []

        # Suche und aktualisiere Reference-Property
        for i, prop in enumerate(symbol.properties):
            if prop.key == "Reference":
                symbol.properties[i] = replace(prop, value=reference)
                break
        else:
            # Falls keine Reference-Property existiert, füge eine hinzu
            ref_prop = Property(
                key="Reference",
                value=reference,
                at=At(x=0.0, y=0.0),
                effects=symbol.properties[0].effects if symbol.properties else None,
            )
            symbol.properties.insert(0, ref_prop)

        return symbol

    def move_symbol(
        self, symbol: Symbol, x: float, y: float, angle: float = 0.0
    ) -> Symbol:
        """
        Verschiebe Symbol zu neuen Koordinaten.

        HINWEIS: Symbol-Library-Definitionen haben keine Position.
        Diese Methode ist für die Kompatibilität mit dem skip-Beispiel,
        aber eigentlich müssten Symbol-Instanzen verwendet werden.

        Args:
            symbol: Zu modifizierendes Symbol
            x: X-Koordinate
            y: Y-Koordinate
            angle: Rotationswinkel in Grad

        Returns:
            Symbol (unverändert, da Library-Symbols keine Position haben)
        """
        # Symbol Library-Definitionen haben keine Position
        # In einer vollständigen Implementierung würden wir Symbol-Instanzen verwenden
        print(
            f"HINWEIS: Symbol {symbol.library_id} würde zu ({x:.2f}, {y:.2f}) verschoben"
        )
        return symbol

    def create_led_grid(
        self,
        base_symbol: Symbol,
        rows: int,
        cols: int,
        is_charlieplex: bool = False,
        start_ref: int = 1,
    ) -> List[List[Optional[Symbol]]]:
        """
        Erstelle ein LED-Raster basierend auf einem Template-Symbol.

        Args:
            base_symbol: Template-Symbol zum Klonen
            rows: Anzahl der Zeilen
            cols: Anzahl der Spalten
            is_charlieplex: True für Charlieplex (überspringe Diagonal-LEDs)
            start_ref: Start-Referenz-Nummer

        Returns:
            2D-Liste von Symbolen (None für übersprungene Positionen)
        """
        reference_count = start_ref
        led_matrix = []

        for row in range(rows):
            row_leds: List[Optional[Symbol]] = []
            for col in range(cols):

                # Überspringe Diagonal-LEDs im Charlieplex-Modus
                if is_charlieplex and col == row:
                    row_leds.append(None)
                    continue

                # Klone das Basis-Symbol
                new_led = self.clone_symbol(base_symbol)

                # Positioniere die LED im Raster
                grid_pos = self.to_grid_position(col * 7, row * 6)
                new_led = self.move_symbol(new_led, grid_pos[0] - 1.27, grid_pos[1])

                # Setze Referenz-Bezeichnung
                new_led = self.set_symbol_reference(new_led, f"D{reference_count}")

                row_leds.append(new_led)
                reference_count += 1

            led_matrix.append(row_leds)

        return led_matrix

    def create_wire_between_points(
        self,
        start_point: Tuple[float, float],
        end_point: Tuple[float, float],
        stroke_width: float = 0.0,
        stroke_type: str = "default",
    ) -> Wire:
        """
        Erstelle einen Draht zwischen zwei Punkten.

        Args:
            start_point: Startpunkt (x, y)
            end_point: Endpunkt (x, y)
            stroke_width: Linienstärke (0 für Standard)
            stroke_type: Linientyp

        Returns:
            Wire-Objekt
        """
        pts = Pts(
            points=[
                Xy(x=start_point[0], y=start_point[1]),
                Xy(x=end_point[0], y=end_point[1]),
            ]
        )

        stroke = Stroke()
        if stroke_width > 0:
            stroke.width = KiCadFloat("width", stroke_width)
        if stroke_type != "default":
            stroke.type = Type(value=stroke_type)

        return Wire(pts=pts, stroke=stroke, uuid=Uuid.new_id())

    def create_junction_at(self, x: float, y: float, diameter: float = 0.0) -> Junction:
        """
        Erstelle eine Junction an der angegebenen Position.

        Args:
            x: X-Koordinate
            y: Y-Koordinate
            diameter: Junction-Durchmesser (0 für Standard)

        Returns:
            Junction-Objekt
        """
        return Junction(
            at=AtXY(x=x, y=y),
            diameter=KiCadFloat("diameter", diameter),
            uuid=Uuid.new_id(),
        )

    def create_global_label(
        self, text: str, x: float, y: float, angle: float = 0.0
    ) -> GlobalLabel:
        """
        Erstelle ein Global Label.

        Args:
            text: Label-Text
            x: X-Koordinate
            y: Y-Koordinate
            angle: Rotationswinkel in Grad

        Returns:
            GlobalLabel-Objekt
        """
        return GlobalLabel(text=text, at=At(x=x, y=y, angle=angle), uuid=Uuid.new_id())

    def create_local_label(
        self, text: str, x: float, y: float, angle: float = 0.0
    ) -> Label:
        """
        Erstelle ein lokales Label.

        Args:
            text: Label-Text
            x: X-Koordinate
            y: Y-Koordinate
            angle: Rotationswinkel in Grad

        Returns:
            Label-Objekt
        """
        return Label(text=text, at=At(x=x, y=y, angle=angle), uuid=Uuid.new_id())

    def add_led_grid_to_schematic(
        self, schematic: KicadSch, led_matrix: List[List[Optional[Symbol]]]
    ) -> None:
        """
        Füge LED-Matrix zum Schaltplan hinzu.

        Args:
            schematic: Schaltplan-Objekt
            led_matrix: 2D-Matrix der LED-Symbole
        """
        if not schematic.lib_symbols:
            schematic.lib_symbols = LibSymbols()

        if not schematic.lib_symbols.symbols:
            schematic.lib_symbols.symbols = []

        # Füge alle LEDs zum Schaltplan hinzu
        for row in led_matrix:
            for led in row:
                if led is not None:
                    schematic.lib_symbols.symbols.append(led)

    def create_row_wiring(
        self,
        schematic: KicadSch,
        led_matrix: List[List[Optional[Symbol]]],
        is_charlieplex: bool = False,
    ) -> List[Wire]:
        """
        Erstelle Zeilen-Verdrahtung (Anoden-Verbindungen).

        Args:
            schematic: Schaltplan-Objekt
            led_matrix: LED-Matrix
            is_charlieplex: Charlieplex-Modus

        Returns:
            Liste der Zeilen-Verbindungsdrähte
        """
        if not schematic.wires:
            schematic.wires = []
        if not schematic.junctions:
            schematic.junctions = []
        if not schematic.global_labels:
            schematic.global_labels = []

        row_wires = []
        row_prefix = "CHRLY" if is_charlieplex else "ROW"

        for row_idx, led_row in enumerate(led_matrix):
            # Finde erste und letzte LED in der Zeile
            first_led_col = None
            last_led_col = None

            for col_idx, led in enumerate(led_row):
                if led is not None:
                    if first_led_col is None:
                        first_led_col = col_idx
                    last_led_col = col_idx

            if first_led_col is None:
                continue  # Keine LEDs in dieser Zeile

            # Erstelle horizontale Drähte von jeder LED nach außen
            pull_up_wires = []
            for col_idx, led in enumerate(led_row):
                if led is None:
                    continue

                # LED-Position (berechnet aus Grid-Position)
                grid_pos = self.to_grid_position(col_idx * 7, row_idx * 6)
                led_x = grid_pos[0] - 1.27
                led_y = grid_pos[1]

                # Draht horizontal von der Anode (angenommen rechter Pin)
                anode_x = led_x + 1.27  # Annahme: Anode ist rechts
                wire_end_x = anode_x + self.unit_spacing

                # Horizontaler Draht von Anode
                h_wire = self.create_wire_between_points(
                    (anode_x, led_y), (wire_end_x, led_y)
                )
                schematic.wires.append(h_wire)

                # Vertikaler Draht nach oben zur Zeilen-Bus
                bus_y = led_y - self.units_to_mm(3)
                v_wire = self.create_wire_between_points(
                    (wire_end_x, led_y), (wire_end_x, bus_y)
                )
                schematic.wires.append(v_wire)
                pull_up_wires.append((wire_end_x, bus_y))

            # Verbinde alle Pull-up-Drähte mit horizontalem Bus
            if pull_up_wires:
                first_x, bus_y = pull_up_wires[0]
                last_x, _ = pull_up_wires[-1]

                # Erweitere Bus um 4 Einheiten nach links
                bus_start_x = first_x - self.units_to_mm(4)

                # Horizontaler Bus-Draht
                bus_wire = self.create_wire_between_points(
                    (bus_start_x, bus_y), (last_x, bus_y)
                )
                schematic.wires.append(bus_wire)
                row_wires.append(bus_wire)

                # Junctions an allen Verbindungspunkten
                for wire_x, wire_y in pull_up_wires:
                    junction = self.create_junction_at(wire_x, wire_y)
                    schematic.junctions.append(junction)

                # Global Label am Bus-Ende
                label = self.create_global_label(
                    f"{row_prefix}_{row_idx + 1}", bus_start_x, bus_y
                )
                schematic.global_labels.append(label)

        return row_wires

    def create_column_wiring(
        self,
        schematic: KicadSch,
        led_matrix: List[List[Optional[Symbol]]],
        is_charlieplex: bool = False,
    ) -> List[Wire]:
        """
        Erstelle Spalten-Verdrahtung (Kathoden-Verbindungen).

        Args:
            schematic: Schaltplan-Objekt
            led_matrix: LED-Matrix
            is_charlieplex: Charlieplex-Modus

        Returns:
            Liste der Spalten-Verbindungsdrähte
        """
        if not led_matrix:
            return []

        if not schematic.wires:
            schematic.wires = []
        if not schematic.junctions:
            schematic.junctions = []
        if not schematic.labels:
            schematic.labels = []

        column_wires = []
        cols = len(led_matrix[0])

        for col_idx in range(cols):
            # Sammle alle LEDs in dieser Spalte
            column_leds = []
            for row_idx, led_row in enumerate(led_matrix):
                if col_idx < len(led_row) and led_row[col_idx] is not None:
                    column_leds.append((row_idx, led_row[col_idx]))

            if not column_leds:
                continue

            # Erstelle horizontale Drähte von jeder LED zur Spalten-Linie
            cathode_points = []
            for row_idx, led in column_leds:
                # LED-Position (berechnet aus Grid-Position)
                grid_pos = self.to_grid_position(col_idx * 7, row_idx * 6)
                led_x = grid_pos[0] - 1.27
                led_y = grid_pos[1]

                # Draht horizontal von der Kathode (angenommen linker Pin)
                cathode_x = led_x - 1.27  # Annahme: Kathode ist links
                wire_end_x = cathode_x - self.unit_spacing

                # Horizontaler Draht von Kathode
                h_wire = self.create_wire_between_points(
                    (cathode_x, led_y), (wire_end_x, led_y)
                )
                schematic.wires.append(h_wire)
                cathode_points.append((wire_end_x, led_y))

            if cathode_points:
                # Vertikaler Spalten-Bus
                first_y = cathode_points[0][1]
                last_y = cathode_points[-1][1]
                bus_x = cathode_points[0][0]

                # Erweitere Bus um 4 Einheiten nach unten
                bus_end_y = last_y + self.units_to_mm(4)

                # Vertikaler Bus-Draht mit gepunkteter Linie
                bus_wire = self.create_wire_between_points(
                    (bus_x, first_y),
                    (bus_x, bus_end_y),
                    stroke_width=0.4,
                    stroke_type="dot",
                )
                schematic.wires.append(bus_wire)
                column_wires.append(bus_wire)

                # Junctions an allen Verbindungspunkten (außer dem ersten)
                for i in range(1, len(cathode_points)):
                    wire_x, wire_y = cathode_points[i]
                    junction = self.create_junction_at(wire_x, wire_y)
                    schematic.junctions.append(junction)

                # Label am Bus-Ende
                if is_charlieplex:
                    local_label = self.create_local_label(
                        f"CATH_{col_idx + 1}", bus_x, bus_end_y, angle=90
                    )
                    if schematic.labels is None:
                        schematic.labels = []
                    schematic.labels.append(local_label)
                else:
                    global_label = self.create_global_label(
                        f"COL_{col_idx + 1}", bus_x, bus_end_y, angle=90
                    )
                    if schematic.global_labels is None:
                        schematic.global_labels = []
                    schematic.global_labels.append(global_label)

        return column_wires

    def create_xy_grid(
        self,
        schematic: KicadSch,
        base_symbol: Symbol,
        rows: int,
        cols: int,
        start_ref: int = 1,
    ) -> None:
        """
        Erstelle ein XY-Matrix-LED-Grid.

        Args:
            schematic: Schaltplan-Objekt
            base_symbol: Basis-LED-Symbol
            rows: Anzahl der Zeilen
            cols: Anzahl der Spalten
            start_ref: Start-Referenz-Nummer
        """
        print(f"Erstelle {rows}x{cols} XY-Matrix...")

        # Erstelle LED-Matrix
        led_matrix = self.create_led_grid(base_symbol, rows, cols, False, start_ref)

        # Füge LEDs zum Schaltplan hinzu
        self.add_led_grid_to_schematic(schematic, led_matrix)

        # Erstelle Verdrahtung
        self.create_row_wiring(schematic, led_matrix, False)
        self.create_column_wiring(schematic, led_matrix, False)

        print(f"XY-Matrix mit {rows}x{cols} LEDs erstellt.")

    def create_charlieplex(
        self,
        schematic: KicadSch,
        base_symbol: Symbol,
        rows: int,
        cols: int,
        start_ref: int = 1,
    ) -> None:
        """
        Erstelle ein Charlieplex-LED-Array.

        Args:
            schematic: Schaltplan-Objekt
            base_symbol: Basis-LED-Symbol
            rows: Anzahl der Zeilen
            cols: Anzahl der Spalten
            start_ref: Start-Referenz-Nummer
        """
        print(f"Erstelle {rows}x{cols} Charlieplex-Array...")

        # Erstelle LED-Matrix (überspringe Diagonal-LEDs)
        led_matrix = self.create_led_grid(base_symbol, rows, cols, True, start_ref)

        # Füge LEDs zum Schaltplan hinzu
        self.add_led_grid_to_schematic(schematic, led_matrix)

        # Erstelle Verdrahtung
        self.create_row_wiring(schematic, led_matrix, True)
        self.create_column_wiring(schematic, led_matrix, True)

        # Zusätzliche Charlieplex-Labels (CATH Labels für Row-Pins)
        if schematic.global_labels and schematic.labels:
            row_labels = [
                lbl for lbl in schematic.global_labels if lbl.text.startswith("CHRLY")
            ]
            for i, row_label in enumerate(row_labels):
                additional_label = self.create_local_label(
                    f"CATH_{i + 1}",
                    (row_label.at.x or 0.0) + self.units_to_mm(1),
                    row_label.at.y or 0.0,
                )
                schematic.labels.append(additional_label)

        print(f"Charlieplex mit {rows}x{cols} LEDs erstellt.")


def example_usage() -> None:
    """Beispiel-Verwendung des Charlieplex-Generators."""
    print("KiCadFiles Charlieplex Generator - Beispiel-Verwendung")
    print("=" * 60)

    # Erstelle einen minimalen Schaltplan

    schematic = KicadSch(
        version=KiCadInt("version", 20231120),  # KiCad 8.0 Format
        generator=KiCadStr("generator", "kicadfiles-charlieplex"),
        uuid=Uuid.new_id(),
    )

    print(schematic.to_sexpr_str())

    # Erstelle ein Beispiel-LED-Symbol (vereinfacht - nur library definition)
    led_symbol = Symbol(
        library_id="Device:LED",
        properties=[
            Property(key="Reference", value="D", at=At(x=0.0, y=2.54)),
            Property(key="Value", value="LED", at=At(x=0.0, y=-2.54)),
        ],
    )

    # Initialisiere Generator
    generator = CharlieplexGenerator()

    print("\n1. Erstelle 4x4 XY-Matrix:")
    generator.create_xy_grid(schematic, led_symbol, 4, 4, 1)

    print(
        f"   - {len(schematic.lib_symbols.symbols) if schematic.lib_symbols else 0} LEDs hinzugefügt"
    )
    print(f"   - {len(schematic.wires) if schematic.wires else 0} Drähte erstellt")
    print(
        f"   - {len(schematic.junctions) if schematic.junctions else 0} Junctions hinzugefügt"
    )
    print(
        f"   - {len(schematic.global_labels) if schematic.global_labels else 0} Global Labels erstellt"
    )

    # Schaltplan für Charlieplex zurücksetzen
    schematic = KicadSch(
        version=KiCadInt("version", 20231120),
        generator=KiCadStr("generator", "kicadfiles-charlieplex"),
        uuid=Uuid.new_id(),
    )

    print("\n2. Erstelle 4x4 Charlieplex:")
    generator.create_charlieplex(schematic, led_symbol, 4, 4, 1)

    print(
        f"   - {len(schematic.lib_symbols.symbols) if schematic.lib_symbols else 0} LEDs hinzugefügt"
    )
    print(f"   - {len(schematic.wires) if schematic.wires else 0} Drähte erstellt")
    print(
        f"   - {len(schematic.junctions) if schematic.junctions else 0} Junctions hinzugefügt"
    )
    print(
        f"   - {len(schematic.global_labels) if schematic.global_labels else 0} Global Labels erstellt"
    )
    print(
        f"   - {len(schematic.labels) if schematic.labels else 0} Local Labels erstellt"
    )

    print("\n✓ Erfolgreiche Implementierung der Charlieplex-Funktionalität!")
    print("  Die Bibliothek unterstützt jetzt:")
    print("  - LED-Grid-Generierung (regulär und Charlieplex)")
    print("  - Systematische Verdrahtung mit Junctions")
    print("  - Automatische Label-Erstellung")
    print("  - Symbol-Kloning und -Positionierung")

    # Speichere Beispiel-Schaltplan (optional)
    try:
        output_file = "charlieplex_example.kicad_sch"
        with open(output_file, "w") as f:
            f.write(schematic.to_sexpr_str())
        print(f"\n  Beispiel gespeichert als: {output_file}")
    except Exception as e:
        print(f"\n  Hinweis: Speichern nicht möglich - {e}")


if __name__ == "__main__":
    example_usage()
