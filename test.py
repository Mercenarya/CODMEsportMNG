import flet as ft
import os
import sys
import pandas as pd
from datetime import time


CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT)
sys.path.append(ROOT)

from config import MEMBERS_PATH, MATCH_PATH, EVENT_PATH, NOTE_PATH

def delete_value():
    pass

def summary_view(page: ft.Page = None):
    '''Displays dashboard analytics overview for the Team'''
    ROOT = os.getcwd()
    MEMBERS_PATH = os.path.join(ROOT, "data", "member1.csv")
    MATCH_PATH = os.path.join(ROOT, "data", "match.csv")
    EVENT_PATH = os.path.join(ROOT, "data", "note.csv")

    total_members_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT)
    total_matches_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)
    total_events_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_ACCENT)
    total_clans_text = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_ACCENT)

    def create_stat_card(title: str, control_text: ft.Text, icon: ft.Icon, border_color: ft.Colors):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([icon, ft.Text(title, size=14, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_500)], spacing=10),
                    ft.Container(height=5),
                    control_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            bgcolor="#20242F",
            border=ft.border.Border.all(1, ft.Colors.GREY_800),
            border_radius=12,
            padding=20,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )

    def update_statistics(e=None):
        if os.path.exists(MEMBERS_PATH):
            try:
                df_mem = pd.read_csv(MEMBERS_PATH, encoding='utf-8-sig')
                df_mem.dropna(how='all', inplace=True)
                total_members_text.value = str(len(df_mem))
            except:
                total_members_text.value = "0"
        else:
            total_members_text.value = "0"

        if os.path.exists(MATCH_PATH):
            try:
                df_match = pd.read_csv(MATCH_PATH, encoding='utf-8-sig')
                df_match.dropna(how='all', inplace=True)
                total_matches_text.value = str(len(df_match))
                
                if 'Clan' in df_match.columns:
                    unique_clans = df_match['Clan'].dropna().unique()
                    total_clans_text.value = str(len(unique_clans))
                else:
                    total_clans_text.value = "0"
            except:
                total_matches_text.value = "0"
                total_clans_text.value = "0"
        else:
            total_matches_text.value = "0"
            total_clans_text.value = "0"

        if os.path.exists(EVENT_PATH):
            try:
                df_event = pd.read_csv(EVENT_PATH, encoding='utf-8-sig')
                df_event.dropna(how='all', inplace=True)
                total_events_text.value = str(len(df_event))
            except:
                total_events_text.value = "0"
        else:
            total_events_text.value = "0"

        try:
            total_members_text.update()
            total_matches_text.update()
            total_events_text.update()
            total_clans_text.update()
        except:
            pass

    update_statistics()

    dashboard_layout = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Icon(ft.Icons.LEADERBOARD_ROUNDED, color=ft.Colors.BLUE_ACCENT, size=28),
                    ft.Text("TEAM ANALYTICS", size=24, weight=ft.FontWeight.BOLD)
                ], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            
            ft.Row(
                controls=[
                    create_stat_card("Total Members", total_members_text, ft.Icon(ft.Icons.PEOPLE_ALT, color=ft.Colors.BLUE_ACCENT), ft.Colors.BLUE_ACCENT),
                    create_stat_card("Total Custom Matches", total_matches_text, ft.Icon(ft.Icons.SPORTS_ESPORTS, color=ft.Colors.GREEN_ACCENT), ft.Colors.GREEN_ACCENT),
                ],
                spacing=20
            ),
            ft.Container(height=10), 
            
            ft.Row(
                controls=[
                    create_stat_card("Total Events", total_events_text, ft.Icon(ft.Icons.EVENT_NOTE, color=ft.Colors.ORANGE_ACCENT), ft.Colors.ORANGE_ACCENT),
                    create_stat_card("Total Opposing Clans", total_clans_text, ft.Icon(ft.Icons.FORT, color=ft.Colors.PURPLE_ACCENT), ft.Colors.PURPLE_ACCENT),
                ],
                spacing=20
            ),
            
            ft.Container(height=20),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Update Statistics", 
                        icon=ft.Icons.REFRESH, 
                        on_click=update_statistics,
                        style=ft.ButtonStyle(bgcolor="#1E293B", color="white")
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        expand=True
    )

    dashboard_layout.custom_refresh = update_statistics
    return dashboard_layout

def members_table(page: ft.Page = None):
    '''Displays member data with structural advanced search filtering'''
    ROOT = os.getcwd() 
    mem_data_list = os.path.join(ROOT, "data", "member1.csv")
    
    editing_index = None
    clan_input = ft.TextField(label="Clan", width=300)
    ingame_input = ft.TextField(label="Nickname (Ingame)", width=300)
    media_input = ft.TextField(label="Media", width=300)
    role_input = ft.TextField(label="Role", width=300)
    note_input = ft.TextField(label="Note", width=300, multiline=True)
    
    search_input = ft.TextField(
        label="Search Keywords",
        border_radius=0,
        width=300,
        bgcolor="grey",
        color="white",
        hint_text="Enter keyword...",
        prefix_icon=ft.Icons.SEARCH,
        on_submit=lambda e: update_table()
    )

    filter_type = ft.Dropdown(
        label="Filter By",
        width=150,
        options=[
            ft.DropdownOption("ingame", text="Nickname"),
            ft.DropdownOption("note", text="Note"),
            ft.DropdownOption("Clan", text="Clan")
        ],
        value="ingame",
        on_select=lambda e: update_table()
    )
    
    search_button = ft.Button(
        "Search",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: update_table(),
        style=ft.ButtonStyle(shape=ft.BeveledRectangleBorder(radius=0)),
        bgcolor="grey",
        color="white",
        height=46
    )
    
    def reset_search(e):
        search_input.value = ""
        filter_type.value = "ingame"
        update_table()
        
    reset_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        on_click=reset_search,
        bgcolor="grey",
    )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("STT")),
            ft.DataColumn(ft.Text("Clan")),
            ft.DataColumn(ft.Text("Nickname")),
            ft.DataColumn(ft.Text("Media")),
            ft.DataColumn(ft.Text("Role")),
            ft.DataColumn(ft.Text("Note")),
            ft.DataColumn(ft.Text("Options"))
        ],
        rows=[]
    )
    
    def close_dialog(e):
        edit_member_dialog.open = False
        
    
    def save_edit_member(e):
        nonlocal editing_index
        if os.path.exists(mem_data_list) and editing_index is not None:
            try:
                df = pd.read_csv(mem_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)

                df.at[editing_index, 'Clan'] = clan_input.value
                df.at[editing_index, 'ingame'] = ingame_input.value
                df.at[editing_index, 'media'] = media_input.value
                df.at[editing_index, 'role'] = role_input.value
                df.at[editing_index, 'note'] = note_input.value

                df.to_csv(mem_data_list, index=False, encoding='utf-8-sig')
                
                page.close_dialog()
                update_table()
            except Exception as ex:
                error_message.value = f"Error saving edits: {str(ex)}"
                error_message.update()
    
    edit_member_dialog = ft.AlertDialog(
        title=ft.Text("Edit Member Information"),
        content=ft.Column(
            controls=[clan_input, ingame_input, media_input, role_input, note_input],
            tight=True, spacing=10
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.ElevatedButton("Save Changes", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_edit_member),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    error_message = ft.Text("", color=ft.Colors.GREY_400, size=13)
    
    def delete_member(row_index):
        if os.path.exists(mem_data_list):
            try:
                df = pd.read_csv(mem_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                df.drop(row_index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                if 'STT' in df.columns:
                    df['STT'] = df.index + 1
                
                df.to_csv(mem_data_list, index=False, encoding='utf-8-sig')
                update_table()
            except Exception as ex:
                error_message.value = f"Error deleting record: {str(ex)}"
                error_message.update()

    def open_edit_dialog(index, current_row_data):
        nonlocal editing_index
        editing_index = index
        
        clan_input.value = str(current_row_data.get('Clan', '')) if pd.notna(current_row_data.get('Clan')) else ''
        ingame_input.value = str(current_row_data.get('ingame', '')) if pd.notna(current_row_data.get('ingame')) else ''
        media_input.value = str(current_row_data.get('media', '')) if pd.notna(current_row_data.get('media')) else ''
        role_input.value = str(current_row_data.get('role', '')) if pd.notna(current_row_data.get('role')) else ''
        note_input.value = str(current_row_data.get('note', '')) if pd.notna(current_row_data.get('note')) else ''
        
        page.show_dialog(edit_member_dialog)
    
    def update_table(e=None):
        if os.path.exists(mem_data_list):
            try:
                df = pd.read_csv(mem_data_list, encoding='utf-8-sig')
                search_keyword = search_input.value.strip().lower()
                target_col = filter_type.value

                if search_keyword and target_col in df.columns:
                    df = df[df[target_col].astype(str).str.lower().str.contains(search_keyword, na=False)]

                data_rows = []
                for index, row in df.iterrows():
                    data_rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(str(row.get('STT', index + 1)))),
                            ft.DataCell(ft.Text(str(row.get('Clan', '')))),
                            ft.DataCell(ft.Text(str(row.get('ingame', '')))),
                            ft.DataCell(ft.Text(str(row.get('media', '')))),
                            ft.DataCell(ft.Text(str(row.get('role', '')))),
                            ft.DataCell(ft.Text(str(row.get('note', '')))),
                            ft.DataCell(ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, on_click=lambda e, idx=index: delete_member(idx)),
                                    ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, on_click=lambda e, idx=index, r=dict(row): open_edit_dialog(idx, r)),
                                ]
                            ))
                        ])
                    )
                table.rows = data_rows
                
                if len(data_rows) == 0 and search_keyword:
                    error_message.value = "No matching members found."
                else:
                    error_message.value = ""
            except Exception as ex:
                error_message.value = f"CSV Reading Error: {str(ex)}"
        else:
            table.rows = []
            error_message.value = "No member records found."
        
        try:
            table.update()
            error_message.update()
        except:
            pass

    update_table()
    
    table_container = ft.Column(
        controls=[
            ft.Row([ft.Text("LIST OF MEMBERS ( IN SERVICE )", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[search_input, filter_type, search_button, reset_button], alignment=ft.MainAxisAlignment.START, spacing=10),
            error_message,
            ft.ListView(controls=[table], expand=True, spacing=10)
        ],
        expand=True
    )
    
    table_container.custom_refresh = update_table 
    return table_container

def match_table(page: ft.Page = None):
    '''Displays match data with dynamic filter search'''
    ROOT = os.getcwd()
    match_data_list = os.path.join(ROOT, "data", "match.csv")
    
    editing_index = None
    
    # --- Edit Dialog Inputs ---
    edit_date = ft.TextField(label="Day", width=90)
    edit_month = ft.TextField(label="Month", width=90)
    edit_year = ft.TextField(label="Year", width=100)
    edit_clan_opponent = ft.TextField(label="Opponent Clan", width=300)
    edit_mode_selection = ft.Dropdown(
        options=[
            ft.DropdownOption(key="Hard point", text="HP"),
            ft.DropdownOption(key="Search & Destroy", text="C4"),
            ft.DropdownOption(key="Domination", text="ABC"),
            ft.DropdownOption(key="Control", text="CT"),
            ft.DropdownOption(key="Team Deathmatch", text="TDM"),
            ft.DropdownOption(key="Frontline", text="FL"),
            ft.DropdownOption(key="Hardpoint & SD", text="HP - C4"),
            ft.DropdownOption(key="Hardpoint, Controls & SD", text="HP - CTs - C4"),
        ],
        width=300, label="Mode"
    )
    edit_note = ft.TextField(label="Note", multiline=True, max_lines=5)
    edit_time_result = ft.TextField(label="Time", width=200)

    def save_edit_time(e):
        if edit_match_time.value:
            edit_time_result.value = f"{edit_match_time.value.hour:02d}:{edit_match_time.value.minute:02d}"
        edit_time_result.update()

    edit_match_time = ft.TimePicker(open=True, entry_mode=ft.TimePickerEntryMode.INPUT_ONLY, on_change=save_edit_time)
    pick_time_button = ft.ElevatedButton("Select Time", on_click=lambda e: page.show_dialog(edit_match_time), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(), color="white", bgcolor="blue"))

    search_input = ft.TextField(
        label="Search Match", width=400, bgcolor="grey", color="white",
        hint_text="Search Opponent Clan, Mode or Note...",
        prefix_icon=ft.Icons.SEARCH, on_submit=lambda e: update_table()
    )
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("STT")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Opponent Clan")),
            ft.DataColumn(ft.Text("Mode")),
            ft.DataColumn(ft.Text("Note")),
            ft.DataColumn(ft.Text("Options"))
        ],
        rows=[]
    )
    
    error_message = ft.Text("", color=ft.Colors.GREY_400, size=13)
    
    def close_dialog(e):
        edit_match_dialog.open = False
        
    def save_edit_match(e):
        nonlocal editing_index
        if os.path.exists(match_data_list) and editing_index is not None:
            try:
                df = pd.read_csv(match_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                
                full_date = f"{edit_date.value}/{edit_month.value}/{edit_year.value}"
                df.at[editing_index, 'Date'] = full_date
                df.at[editing_index, 'Time'] = edit_time_result.value
                df.at[editing_index, 'Clan'] = edit_clan_opponent.value
                df.at[editing_index, 'Mode'] = edit_mode_selection.value
                df.at[editing_index, 'Note'] = edit_note.value
                
                df.to_csv(match_data_list, index=False, encoding='utf-8-sig')
                
                edit_match_dialog.open = False
                update_table()
            except Exception as ex:
                error_message.value = f"Error editing match: {str(ex)}"
                error_message.update()

    edit_match_dialog = ft.AlertDialog(
        title=ft.Text("Edit Custom Match Record"),
        content=ft.Column(controls=[
            ft.Row([edit_date, edit_month, edit_year]), 
            ft.Row([pick_time_button, edit_time_result]), 
            edit_clan_opponent, edit_mode_selection, edit_note
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.ElevatedButton("Save Changes", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_edit_match),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_edit_dialog(index, current_row_data):
        nonlocal editing_index
        editing_index = index
        
        raw_date = str(current_row_data.get('Date', '//'))
        date_parts = raw_date.split('/') if '/' in raw_date else ['', '', '']
        while len(date_parts) < 3: date_parts.append('')
            
        edit_date.value = date_parts[0]
        edit_month.value = date_parts[1]
        edit_year.value = date_parts[2]
        
        edit_time_result.value = str(current_row_data.get('Time', '00:00'))
        edit_clan_opponent.value = str(current_row_data.get('Clan', ''))
        edit_mode_selection.value = current_row_data.get('Mode', None)
        edit_note.value = str(current_row_data.get('Note', ''))
        
        page.show_dialog(edit_match_dialog)

    def delete_match(row_index):
        if os.path.exists(match_data_list):
            try:
                df = pd.read_csv(match_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                df.drop(row_index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                if 'STT' in df.columns:
                    df['STT'] = df.index + 1
                df.to_csv(match_data_list, index=False, encoding='utf-8-sig')
                update_table()
            except Exception as ex:
                error_message.value = f"Error deleting match: {str(ex)}"
                error_message.update()

    def update_table(e=None):
        if os.path.exists(match_data_list):
            try:
                df = pd.read_csv(match_data_list, encoding='utf-8-sig')
                keyword = search_input.value.strip().lower()
                if keyword:
                    df = df[
                        (df['Clan'].astype(str).str.lower().str.contains(keyword, na=False)) |
                        (df['Mode'].astype(str).str.lower().str.contains(keyword, na=False)) |
                        (df['Note'].astype(str).str.lower().str.contains(keyword, na=False))
                    ]
                
                data_rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(str(row.get('Date', '')))),
                        ft.DataCell(ft.Text(str(row.get('Time', '')))),
                        ft.DataCell(ft.Text(str(row.get('Clan', '')))),
                        ft.DataCell(ft.Text(str(row.get('Mode', '')))),
                        ft.DataCell(ft.Text(str(row.get('Note', '')))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, on_click=lambda e, idx=index: delete_match(idx)),
                            ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, on_click=lambda e, idx=index, r=dict(row): open_edit_dialog(idx, r)),
                        ]))
                    ]) for index, row in df.iterrows()
                ]
                table.rows = data_rows
                error_message.value = "" if data_rows else "No matching results."
            except Exception as ex:
                error_message.value = f"Error processing match CSV: {str(ex)}"
        else:
            table.rows = []
            error_message.value = "No match history found."
        try:
            table.update()
            error_message.update()
        except:
            pass

    update_table()
    
    table_container = ft.Column(
        controls=[
            ft.Row([ft.Text("LIST OF MATCHES ( DAILY CUSTOM )", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([search_input, ft.IconButton(ft.Icons.REFRESH, on_click=lambda e: [setattr(search_input, 'value', ''), update_table()])], spacing=10),
            error_message,
            ft.ListView(controls=[table], expand=True, spacing=10)
        ],
        expand=True
    )
    table_container.custom_refresh = update_table 
    return table_container

def event_table(page: ft.Page = None):
    '''Displays system events table with search query capabilities'''
    ROOT = os.getcwd()
    event_data_list = os.path.join(ROOT, "data", "events.csv")
    
    editing_index = None
    
    # --- Edit Dialog Inputs ---
    edit_date_event = ft.TextField(label="Day", width=90)
    edit_month_event = ft.TextField(label="Month", width=90)
    edit_year_event = ft.TextField(label="Year", width=100)
    edit_event_name = ft.TextField(label="Event Title")
    edit_event_content = ft.TextField(label="Content Summary", multiline=True, min_lines=3)

    search_input = ft.TextField(
        label="Search Events", width=400, bgcolor="grey", color="white",
        hint_text="Search event name or content details...",
        prefix_icon=ft.Icons.SEARCH, on_submit=lambda e: update_table()
    )
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("STT")),
            ft.DataColumn(ft.Text("Event")),
            ft.DataColumn(ft.Text("Content")),
            ft.DataColumn(ft.Text("Timeline")),
            ft.DataColumn(ft.Text("Options"))
        ],
        rows=[]
    )
    
    error_message = ft.Text("", color=ft.Colors.GREY_400, size=13)
    
    def close_dialog(e):
        edit_event_dialog.open = False
        
        
    def save_edit_event(e):
        nonlocal editing_index
        if os.path.exists(event_data_list) and editing_index is not None:
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                
                full_date = f"{edit_date_event.value}/{edit_month_event.value}/{edit_year_event.value}"
                df.at[editing_index, 'name'] = edit_event_name.value
                df.at[editing_index, 'content'] = edit_event_content.value
                df.at[editing_index, 'date'] = full_date
                
                df.to_csv(event_data_list, index=False, encoding='utf-8-sig')
                
                edit_event_dialog.open = False
                update_table()
            except Exception as ex:
                error_message.value = f"Error saving event changes: {str(ex)}"
                error_message.update()

    edit_event_dialog = ft.AlertDialog(
        title=ft.Text("Modify Event Details"),
        content=ft.Column(controls=[
            ft.Row([edit_date_event, edit_month_event, edit_year_event]), 
            edit_event_name, edit_event_content
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_edit_event),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_edit_dialog(index, current_row_data):
        nonlocal editing_index
        editing_index = index
        
        raw_date = str(current_row_data.get('date', '//'))
        date_parts = raw_date.split('/') if '/' in raw_date else ['', '', '']
        while len(date_parts) < 3: date_parts.append('')
            
        edit_date_event.value = date_parts[0]
        edit_month_event.value = date_parts[1]
        edit_year_event.value = date_parts[2]
        
        edit_event_name.value = str(current_row_data.get('name', ''))
        edit_event_content.value = str(current_row_data.get('content', ''))
        
        page.show_dialog(edit_event_dialog)

    def delete_event(row_index):
        if os.path.exists(event_data_list):
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                df.drop(row_index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                if 'STT' in df.columns:
                    df['STT'] = df.index + 1
                df.to_csv(event_data_list, index=False, encoding='utf-8-sig')
                update_table()
            except Exception as ex:
                error_message.value = f"Error removing event: {str(ex)}"
                error_message.update()

    def update_table(e=None):
        if os.path.exists(event_data_list):
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                keyword = search_input.value.strip().lower()
                if keyword:
                    df = df[
                        (df['name'].astype(str).str.lower().str.contains(keyword, na=False)) |
                        (df['content'].astype(str).str.lower().str.contains(keyword, na=False))
                    ]
                
                data_rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(index + 1))),
                        ft.DataCell(ft.Text(str(row.get('name', '')))),
                        ft.DataCell(ft.Text(str(row.get('content', '')))),
                        ft.DataCell(ft.Text(str(row.get('date', '')))),
                        ft.DataCell(ft.Row([
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, on_click=lambda e, idx=index: delete_event(idx)),
                            ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, on_click=lambda e, idx=index, r=dict(row): open_edit_dialog(idx, r)),
                        ]))
                    ]) for index, row in df.iterrows()
                ]
                table.rows = data_rows
                error_message.value = "" if data_rows else "No events match criteria."
            except Exception as ex:
                error_message.value = f"Error pulling events: {str(ex)}"
        else:
            table.rows = []
            error_message.value = "No historical events documented."
        try:
            table.update()
            error_message.update()
        except:
            pass

    update_table()
    
    table_container = ft.Column(
        controls=[
            ft.Row([ft.Text("LIST OF EVENTS ( MONTH - DAILY )", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([search_input, ft.IconButton(ft.Icons.REFRESH, on_click=lambda e: [setattr(search_input, 'value', ''), update_table()])], spacing=10),
            error_message,
            ft.ListView(controls=[table], expand=True, spacing=10)
        ],
        expand=True
    )
    table_container.custom_refresh = update_table 
    return table_container

def event_cards_view(page: ft.Page = None):
    '''Renders note board panel configuration with lookup search engine filters'''
    ROOT = os.getcwd()
    event_data_list = os.path.join(ROOT, "data", "notes.csv")
    
    editing_index = None
    
    # --- Edit Dialog Inputs ---
    edit_date_note = ft.TextField(label="Day", width=90)
    edit_month_note = ft.TextField(label="Month", width=90)
    edit_year_note = ft.TextField(label="Year", width=100)
    edit_note_title = ft.TextField(label="Note Title")
    edit_note_content = ft.TextField(label="Detailed Notes", multiline=True, min_lines=3)

    search_input = ft.TextField(
        label="Search Notes", width=400, bgcolor="grey", color="white",
        hint_text="Type to find note topics or content...",
        prefix_icon=ft.Icons.SEARCH, on_change=lambda e: update_cards()
    )
    
    cards_grid = ft.GridView(
        expand=True, runs_count=3, max_extent=460,
        child_aspect_ratio=1.3, spacing=15, run_spacing=15,
    )
    
    error_message = ft.Text("", color=ft.Colors.GREY_400, size=13)
    
    def close_dialog(e):
        edit_note_dialog.open = False
        
    def save_edit_note(e):
        nonlocal editing_index
        if os.path.exists(event_data_list) and editing_index is not None:
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                
                full_date = f"{edit_date_note.value}/{edit_month_note.value}/{edit_year_note.value}"
                df.at[editing_index, 'name'] = edit_note_title.value
                df.at[editing_index, 'content'] = edit_note_content.value
                df.at[editing_index, 'date'] = full_date
                
                df.to_csv(event_data_list, index=False, encoding='utf-8-sig')
                
                edit_note_dialog.open = False
                update_cards()
            except Exception as ex:
                error_message.value = f"Error saving note adjustment: {str(ex)}"
                error_message.update()

    edit_note_dialog = ft.AlertDialog(
        title=ft.Text("Edit Note Structure"),
        content=ft.Column(controls=[
            ft.Row([edit_date_note, edit_month_note, edit_year_note]), 
            edit_note_title, edit_note_content
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_edit_note),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_edit_dialog(index, current_row_data):
        nonlocal editing_index
        editing_index = index
        
        raw_date = str(current_row_data.get('date', '//'))
        date_parts = raw_date.split('/') if '/' in raw_date else ['', '', '']
        while len(date_parts) < 3: date_parts.append('')
            
        edit_date_note.value = date_parts[0]
        edit_month_note.value = date_parts[1]
        edit_year_note.value = date_parts[2]
        
        edit_note_title.value = str(current_row_data.get('name', ''))
        edit_note_content.value = str(current_row_data.get('content', ''))
        
        page.show_dialog(edit_note_dialog)

    def delete_event(row_index):
        if os.path.exists(event_data_list):
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                df.dropna(how='all', inplace=True)
                df.drop(row_index, inplace=True)
                df.reset_index(drop=True, inplace=True)
                if 'STT' in df.columns:
                    df['STT'] = df.index + 1
                df.to_csv(event_data_list, index=False, encoding='utf-8-sig')
                update_cards()
            except Exception as ex:
                error_message.value = f"Error updating note list: {str(ex)}"
                error_message.update()

    def update_cards(e=None):
        if os.path.exists(event_data_list):
            try:
                df = pd.read_csv(event_data_list, encoding='utf-8-sig')
                keyword = search_input.value.strip().lower()
                if keyword:
                    df = df[
                        (df['name'].astype(str).str.lower().str.contains(keyword, na=False)) |
                        (df['content'].astype(str).str.lower().str.contains(keyword, na=False))
                    ]

                new_cards = []
                for index, row in df.iterrows():
                    evt_stt = str(index + 1)
                    evt_name = str(row.get('name', 'No Title'))
                    evt_content = str(row.get('content', ''))
                    evt_date = str(row.get('date', ''))
                    
                    card = ft.Container(
                        width=700, height=300, bgcolor="#20242F",
                        border=ft.border.Border.all(1, ft.Colors.GREY_800),
                        border_radius=12, padding=15,
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Row([
                                            ft.Text(f"#{evt_stt}", size=12, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
                                            ft.Text(evt_name, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200, overflow=ft.TextOverflow.ELLIPSIS),
                                        ], width=500, spacing=5, expand=True),
                                        ft.Row([
                                            ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, icon_size=18, on_click=lambda e, idx=index, r=dict(row): open_edit_dialog(idx, r)),
                                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, icon_size=18, on_click=lambda e, idx=index: delete_event(idx)),
                                        ], spacing=0)
                                    ], width=500
                                ),
                                ft.Divider(height=1, color=ft.Colors.GREY_800),
                                ft.Container(
                                    width=500, height=300, content=ft.Text(evt_content, size=13, color=ft.Colors.GREY_300),
                                    expand=True, alignment=ft.alignment.Alignment.TOP_LEFT,
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=12, color=ft.Colors.GREY_500),
                                        ft.Text(evt_date, size=11, color=ft.Colors.GREY_500, italic=True)
                                    ]
                                )
                            ]
                        )
                    )
                    new_cards.append(card)
                cards_grid.controls = new_cards
                error_message.value = "" if new_cards else "No matching entries found."
            except Exception as ex:
                error_message.value = f"Error pulling card views: {str(ex)}"
        else:
            cards_grid.controls = []
            error_message.value = "No existing annotations found."
        try:
            cards_grid.update()
            error_message.update()
        except:
            pass

    update_cards()
    
    table_container = ft.Column(
        controls=[
            ft.Row([ft.Icon(ft.Icons.NOTE_ALT_OUTLINED, color=ft.Colors.BLUE_ACCENT), ft.Text("BOARD OF EVENTS & NOTES", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([search_input], alignment=ft.MainAxisAlignment.START),
            error_message,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            cards_grid
        ],
        expand=True
    )
    table_container.custom_refresh = update_cards 
    return table_container

def academy_tier_selector(page: ft.Page = None):
    '''Academy Management Portal managing primary and secondary team structures with full CRUD capabilities'''
    ROOT = os.getcwd()
    selected_tier = None
    main_layout = ft.Container(expand=True)

    # --- Inputs for Add / Edit Actions ---
    input_ingame = ft.TextField(label="Ingame (Nickname)", width=300)
    input_role = ft.TextField(label="Role (Sniper, Attacker...)", value="Striker", width=300)
    input_status = ft.Dropdown(label="Status", width=300, options=[ft.DropdownOption("Main"), ft.DropdownOption("Substitute"), ft.DropdownOption("Away")])
    input_kda = ft.TextField(label="KDA", width=300, value="0.0")
    input_mvp = ft.TextField(label="MVP", width=300, value="0")

    input_tac_title = ft.TextField(label="Tactics & Reviews", width=300)
    input_tac_category = ft.Dropdown(label="Class", width=300, options=[ft.DropdownOption("Tactics"), ft.DropdownOption("VOD Review")])
    input_tac_map = ft.TextField(label="Map's type", width=300)
    input_tac_url = ft.TextField(label="Link Video (YouTube/Drive URL)", width=300, value="https://")

    input_sch_title = ft.TextField(label="Scrims / Tournaments", width=300)
    input_sch_opponent = ft.TextField(label="Opponent", width=300)
    input_sch_datetime = ft.TextField(label="Timeline", width=300)
    input_sch_result = ft.Dropdown(label="Initial Result", width=300, options=[ft.DropdownOption("Upcoming"), ft.DropdownOption("Win"), ft.DropdownOption("Loss")])

    editing_academy_index = None
    current_refresh_callback = None

    def close_dialog(e=None):
        add_member_dialog.open = False
        add_tactic_dialog.open = False
        add_schedule_dialog.open = False
        page.update()

    # =========================================================================
    # TAB 1: ACADEMY MEMBERS
    # =========================================================================
    def build_personnel_tab(tier_name):
        filename = "primus_members.csv" if "Primus" in tier_name else "aspirants_members.csv"
        csv_path = os.path.join(ROOT, "data", filename)
        
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            pd.DataFrame(columns=['STT', 'ingame', 'tactical_role', 'status', 'kda', 'mvp_count']).to_csv(csv_path, index=False, encoding='utf-8-sig')

        search_member_input = ft.TextField(label="Search Players", hint_text="Enter Nickname or Role...", width=300, prefix_icon=ft.Icons.SEARCH, on_change=lambda e: load_members())
        members_list = ft.ListView(expand=True, spacing=10)

        def delete_academy_member(idx):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.drop(idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df['STT'] = df.index + 1
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            load_members()

        def open_edit_academy_member(idx, row_data):
            nonlocal editing_academy_index
            editing_academy_index = idx
            input_ingame.value = str(row_data.get('ingame', ''))
            input_role.value = str(row_data.get('tactical_role', ''))
            input_status.value = str(row_data.get('status', 'Main'))
            input_kda.value = str(row_data.get('kda', '0.0'))
            input_mvp.value = str(row_data.get('mvp_count', '0'))
            
            add_member_dialog.title = ft.Text("Edit Player Information")
            add_member_dialog.actions[1].on_click = perform_edit_member
            page.show_dialog(add_member_dialog)

        def perform_edit_member(e):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.at[editing_academy_index, 'ingame'] = input_ingame.value
            df.at[editing_academy_index, 'tactical_role'] = input_role.value
            df.at[editing_academy_index, 'status'] = input_status.value
            df.at[editing_academy_index, 'kda'] = input_kda.value
            df.at[editing_academy_index, 'mvp_count'] = input_mvp.value
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            close_dialog()
            load_members()

        def load_members():
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            keyword = search_member_input.value.strip().lower()
            if keyword:
                df = df[
                    (df['ingame'].astype(str).str.lower().str.contains(keyword, na=False)) |
                    (df['tactical_role'].astype(str).str.lower().str.contains(keyword, na=False))
                ]
            cards = []
            for idx, row in df.iterrows():
                cards.append(
                    ft.Container(
                        bgcolor="#1A1C23", border=ft.border.Border.all(1, ft.Colors.GREY_800),
                        border_radius=10, padding=12,
                        content=ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.AMBER_400 if "Primus" in tier_name else ft.Colors.BLUE_400, size=30),
                            ft.Column([
                                ft.Text(str(row.get('ingame', 'N/A')), size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Role: {row.get('tactical_role', 'Not specified')} | Status: {row.get('status', 'Main')}", size=12, color=ft.Colors.GREY_400)
                            ], expand=True),
                            ft.Row([
                                ft.Container(content=ft.Text(f"KDA: {row.get('kda', '0.0')}", size=12, weight=ft.FontWeight.W_500), bgcolor=ft.Colors.GREY_900, padding=6, border_radius=5),
                                ft.Container(content=ft.Text(f"⭐ MVP: {row.get('mvp_count', '0')}", size=12, weight=ft.FontWeight.W_500), bgcolor=ft.Colors.GREY_900, padding=6, border_radius=5),
                                ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, icon_size=16, on_click=lambda e, idx=idx, r=dict(row): open_edit_academy_member(idx, r)),
                                ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, icon_size=16, on_click=lambda e, idx=idx: delete_academy_member(idx)),
                            ], spacing=8)
                        ])
                    )
                )
            members_list.controls = cards if cards else [ft.Text("List is empty", color=ft.Colors.GREY_500)]
            try: members_list.update()
            except: pass

        nonlocal current_refresh_callback
        current_refresh_callback = load_members

        def trigger_add_member(e):
            input_ingame.value = ""
            input_role.value = "Striker"
            input_status.value = "Main"
            input_kda.value = "0.0"
            input_mvp.value = "0"
            add_member_dialog.title = ft.Text("New Player / Member")
            add_member_dialog.actions[1].on_click = save_member_data
            page.show_dialog(add_member_dialog)

        view = ft.Column([
            ft.Row([
                ft.Text("Players's list", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([search_member_input, ft.Button("Add Player", icon=ft.Icons.PERSON_ADD, on_click=trigger_add_member)])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.GREY_800),
            members_list
        ], expand=True)
        
        load_members()
        return view

    # =========================================================================
    # TAB 2: ACADEMY TACTICS
    # =========================================================================
    def build_tactics_tab(tier_name):
        filename = "team_1.csv" if "Primus" in tier_name else "team_2.csv"
        csv_path = os.path.join(ROOT, "data", filename)
        
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            pd.DataFrame(columns=['STT', 'title', 'category', 'map_name', 'media_url']).to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        search_tac_input = ft.TextField(label="Search Tactics", hint_text="Enter title or map name...", width=300, prefix_icon=ft.Icons.SEARCH, on_change=lambda e: load_tactics())
        tactics_grid = ft.GridView(expand=True, max_extent=300, spacing=15, run_spacing=15, child_aspect_ratio=1.3)

        def delete_tactic(idx):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.drop(idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df['STT'] = df.index + 1
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            load_tactics()

        def open_edit_tactic(idx, row_data):
            nonlocal editing_academy_index
            editing_academy_index = idx
            input_tac_title.value = str(row_data.get('title', ''))
            input_tac_category.value = str(row_data.get('category', 'Tactics'))
            input_tac_map.value = str(row_data.get('map_name', ''))
            input_tac_url.value = str(row_data.get('media_url', ''))
            
            add_tactic_dialog.title = ft.Text("Edit Tactic/VOD Record")
            add_tactic_dialog.actions[1].on_click = perform_edit_tactic
            page.show_dialog(add_tactic_dialog)

        def perform_edit_tactic(e):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.at[editing_academy_index, 'title'] = input_tac_title.value
            df.at[editing_academy_index, 'category'] = input_tac_category.value
            df.at[editing_academy_index, 'map_name'] = input_tac_map.value
            df.at[editing_academy_index, 'media_url'] = input_tac_url.value
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            close_dialog()
            load_tactics()

        def load_tactics():
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            keyword = search_tac_input.value.strip().lower()
            if keyword:
                df = df[
                    (df['title'].astype(str).str.lower().str.contains(keyword, na=False)) |
                    (df['map_name'].astype(str).str.lower().str.contains(keyword, na=False))
                ]
            items = []
            for idx, row in df.iterrows():
                items.append(
                    ft.Container(
                        bgcolor="#20242F", padding=15, border_radius=8,
                        border=ft.border.Border.all(1, ft.Colors.GREY_800),
                        content=ft.Column([
                            ft.Row([
                                ft.Container(content=ft.Text(str(row.get('category', 'VOD')).upper(), size=10, color="white"), bgcolor=ft.Colors.BLUE_900, padding=4, border_radius=4),
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_size=16, icon_color=ft.Colors.BLUE_300, on_click=lambda e, idx=idx, r=dict(row): open_edit_tactic(idx, r)),
                                    ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=16, icon_color=ft.Colors.RED_300, on_click=lambda e, idx=idx: delete_tactic(idx))
                                ], spacing=0)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(str(row.get('title', 'Tactic Record')), size=14, weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Row([
                                ft.Row([ft.Icon(ft.Icons.MAP, size=14, color=ft.Colors.GREY_500), ft.Text(str(row.get('map_name', 'All')), size=11, color=ft.Colors.GREY_400)]),
                                ft.IconButton(icon=ft.Icons.LINK, icon_size=16, icon_color=ft.Colors.BLUE_ACCENT, url=str(row.get('media_url', '#')))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ])
                    )
                )
            tactics_grid.controls = items if items else [ft.Text("No tactics available.", color=ft.Colors.GREY_500)]
            try: tactics_grid.update()
            except: pass

        nonlocal current_refresh_callback
        current_refresh_callback = load_tactics

        def trigger_add_tactic(e):
            input_tac_title.value = ""
            input_tac_category.value = "Tactics"
            input_tac_map.value = ""
            input_tac_url.value = "https://"
            add_tactic_dialog.title = ft.Text("New Tactic / VOD Review")
            add_tactic_dialog.actions[1].on_click = save_tactic_data
            page.show_dialog(add_tactic_dialog)

        view = ft.Column([
            ft.Row([
                ft.Text("TACTICS & VOD REVIEWS", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([search_tac_input, ft.Button("Add Tactic/VOD", icon=ft.Icons.LIGHTBULB, on_click=trigger_add_tactic)])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.GREY_800),
            tactics_grid
        ], expand=True)
        load_tactics()
        return view

    # =========================================================================
    # TAB 3: ACADEMY SCHEDULE
    # =========================================================================
    def build_schedule_tab(tier_name):
        filename = "primus_schedule.csv" if "Primus" in tier_name else "aspirants_schedule.csv"
        csv_path = os.path.join(ROOT, "data", filename)
        
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            pd.DataFrame(columns=['STT', 'type', 'title', 'opponent', 'date_time', 'result']).to_csv(csv_path, index=False, encoding='utf-8-sig')

        search_sch_input = ft.TextField(label="Search Schedules", hint_text="Enter match title or opponent...", width=300, prefix_icon=ft.Icons.SEARCH, on_change=lambda e: load_schedule())
        schedule_list = ft.ListView(expand=True, spacing=10)

        def delete_schedule(idx):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.drop(idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df['STT'] = df.index + 1
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            load_schedule()

        def open_edit_schedule(idx, row_data):
            nonlocal editing_academy_index
            editing_academy_index = idx
            input_sch_title.value = str(row_data.get('title', ''))
            input_sch_opponent.value = str(row_data.get('opponent', ''))
            input_sch_datetime.value = str(row_data.get('date_time', ''))
            input_sch_result.value = str(row_data.get('result', 'Upcoming'))
            
            add_schedule_dialog.title = ft.Text("Edit Schedule / Scrim")
            add_schedule_dialog.actions[1].on_click = perform_edit_schedule
            page.show_dialog(add_schedule_dialog)

        def perform_edit_schedule(e):
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            df.at[editing_academy_index, 'title'] = input_sch_title.value
            df.at[editing_academy_index, 'opponent'] = input_sch_opponent.value
            df.at[editing_academy_index, 'date_time'] = input_sch_datetime.value
            df.at[editing_academy_index, 'result'] = input_sch_result.value
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            close_dialog()
            load_schedule()

        def load_schedule():
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
            keyword = search_sch_input.value.strip().lower()
            if keyword:
                df = df[
                    (df['title'].astype(str).str.lower().str.contains(keyword, na=False)) |
                    (df['opponent'].astype(str).str.lower().str.contains(keyword, na=False))
                ]
            items = []
            for idx, row in df.iterrows():
                is_win = "Win" in str(row.get('result', ''))
                items.append(
                    ft.Container(
                        bgcolor="#14171F", padding=15, border_radius=10,
                        border=ft.border.Border.all(1, ft.Colors.GREY_800),
                        content=ft.Row([
                            ft.Column([
                                ft.Text(str(row.get('date_time', 'Unknown')), size=12, color=ft.Colors.GREY_500),
                                ft.Text(str(row.get('title', 'Match')), size=15, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Opponent: {row.get('opponent', 'Unknown')}", size=13, color=ft.Colors.GREY_400),
                            ], expand=True),
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(str(row.get('result', 'Upcoming')), size=12, weight=ft.FontWeight.BOLD, color="white"),
                                    bgcolor=ft.Colors.GREEN_700 if is_win else (ft.Colors.GREY_800 if "Upcoming" in str(row.get('result', '')) else ft.Colors.RED_700),
                                    padding=8, border_radius=6
                                ),
                                ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.BLUE, on_click=lambda e, idx=idx, r=dict(row): open_edit_schedule(idx, r)),
                                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, on_click=lambda e, idx=idx: delete_schedule(idx))
                            ], spacing=5)
                        ])
                    )
                )
            schedule_list.controls = items if items else [ft.Text("No upcoming matches found.", color=ft.Colors.GREY_500)]
            try: schedule_list.update()
            except: pass

        nonlocal current_refresh_callback
        current_refresh_callback = load_schedule

        def trigger_add_schedule(e):
            input_sch_title.value = ""
            input_sch_opponent.value = ""
            input_sch_datetime.value = ""
            input_sch_result.value = "Upcoming"
            add_schedule_dialog.title = ft.Text("New Schedule / Scrim")
            add_schedule_dialog.actions[1].on_click = save_schedule_data
            page.show_dialog(add_schedule_dialog)

        view = ft.Column([
            ft.Row([
                ft.Text("Schedule & Training (SCRIMS)", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([search_sch_input, ft.Button("New Schedule", icon=ft.Icons.CALENDAR_TODAY, on_click=trigger_add_schedule)])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.GREY_800),
            schedule_list
        ], expand=True)
        load_schedule()
        return view

    # =========================================================================
    # TAB 4: STATISTICS & AI INSIGHTS (YÊU CẦU MỚI BỔ SUNG)
    # =========================================================================
    def build_statistics_tab(tier_name):
        filename = "primus_members.csv" if "Primus" in tier_name else "aspirants_members.csv"
        csv_path = os.path.join(ROOT, "data", filename)

        # Đọc dữ liệu từ file CSV thành viên
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            df = pd.read_csv(csv_path, encoding='utf-8-sig').dropna(how='all')
        else:
            df = pd.DataFrame(columns=['STT', 'ingame', 'tactical_role', 'status', 'kda', 'mvp_count'])

        # Xử lý tính toán số liệu thống kê cơ bản
        total_players = len(df)
        df['kda'] = pd.to_numeric(df['kda'], errors='coerce').fillna(0.0)
        df['mvp_count'] = pd.to_numeric(df['mvp_count'], errors='coerce').fillna(0)

        avg_kda = df['kda'].mean() if total_players > 0 else 0.0
        total_mvp = df['mvp_count'].sum() if total_players > 0 else 0

        # Phân loại KDA theo các tiêu chí yêu cầu
        under_1 = len(df[df['kda'] < 1.0])
        mid_1_15 = len(df[(df['kda'] >= 1.0) & (df['kda'] < 1.5)])
        high_15_2 = len(df[(df['kda'] >= 1.5) & (df['kda'] < 2.0)])
        pro_2_plus = len(df[df['kda'] >= 2.0])

        # Cấu hình các lát của Biểu đồ Tròn (Pie Chart)
        chart_sections = []
        if total_players == 0:
            chart_sections.append(ft.PieChartSection(100, title="No Data", color=ft.Colors.GREY_600, radius=50))
        else:
            if under_1 > 0:
                chart_sections.append(ft.PieChartSection(under_1, title=f"Dưới TB\n({under_1})", color=ft.Colors.RED_600, radius=50, title_style=ft.TextStyle(size=10, weight="bold")))
            if mid_1_15 > 0:
                chart_sections.append(ft.PieChartSection(mid_1_15, title=f"Trung Bình\n({mid_1_15})", color=ft.Colors.ORANGE_600, radius=50, title_style=ft.TextStyle(size=10, weight="bold")))
            if high_15_2 > 0:
                chart_sections.append(ft.PieChartSection(high_15_2, title=f"Khá\n({high_15_2})", color=ft.Colors.BLUE_600, radius=50, title_style=ft.TextStyle(size=10, weight="bold")))
            if pro_2_plus > 0:
                chart_sections.append(ft.PieChartSection(pro_2_plus, title=f"Giỏi/Rank Cao\n({pro_2_plus})", color=ft.Colors.GREEN_600, radius=50, title_style=ft.TextStyle(size=10, weight="bold")))

        pie_chart = ft.PieChart(
            sections=chart_sections,
            sections_space=2,
            center_space_radius=40,
            expand=True
        )

        # Thiết lập Prompt Sẵn dựa trên chỉ số thực tế
        ai_prompt_template = (
            f"=== SYSTEM PERFORMANCE EVALUATION PROMPT ===\n"
            f"Context: Analyzing performance metrics for roster '{tier_name}'.\n"
            f"Current Roster Size: {total_players} players.\n"
            f"Squad Average KDA: {avg_kda:.2f}\n"
            f"Total Accumulated MVPs: {total_mvp}\n\n"
            f"Distribution Breakdown:\n"
            f"- KDA < 1.00 (Below Average): {under_1} players\n"
            f"- KDA 1.00 - 1.50 (Average): {mid_1_15} players\n"
            f"- KDA 1.50 - 2.00 (Above Average): {high_15_2} players\n"
            f"- KDA >= 2.00 (Elite / High Rank Impact): {pro_2_plus} players\n\n"
            f"Task: Generate a strategic squad evaluation focusing on bottlenecks and tactical tiering."
        )

        ai_input_field = ft.TextField(
            label="AI Prompt Generation & Evaluation Context",
            value=ai_prompt_template,
            multiline=True,
            min_lines=8,
            max_lines=12,
            expand=True,
            text_size=13,
        )

        # Layout hiển thị chính của tab Thống kê
        view = ft.Column([
            ft.Text("ACADEMY SQUAD STATISTICS", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(color=ft.Colors.GREY_800),
            
            # Khối hiển thị Tổng quan nhanh (Cards)
            ft.Row([
                ft.Container(
                    content=ft.Column([ft.Text("Avg KDA", size=12, color=ft.Colors.GREY_400), ft.Text(f"{avg_kda:.2f}", size=20, weight="bold", color=ft.Colors.AMBER_400)]),
                    bgcolor="#1A1C23", padding=15, border_radius=8, expand=True
                ),
                ft.Container(
                    content=ft.Column([ft.Text("Total MVPs", size=12, color=ft.Colors.GREY_400), ft.Text(f"{total_mvp}", size=20, weight="bold", color=ft.Colors.BLUE_400)]),
                    bgcolor="#1A1C23", padding=15, border_radius=8, expand=True
                ),
            ], spacing=15),
            
            # Khối Đồ thị & Prompt AI chia đôi không gian
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("KDA Tier Distribution Diagram", size=14, weight="bold"),
                        ft.Container(content=pie_chart, height=200, alignment=ft.alignment.center)
                    ]),
                    bgcolor="#1A1C23", padding=15, border_radius=8, expand=4
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("AI Analytical Playground", size=14, weight="bold"),
                        ai_input_field,
                        ft.ElevatedButton("Request AI Evaluation", icon=ft.Icons.AUTO_AWESOME, bgcolor=ft.Colors.BLUE_800, color="white")
                    ], expand=True),
                    bgcolor="#1A1C23", padding=15, border_radius=8, expand=6
                )
            ], spacing=15, expand=True)
        ], expand=True, spacing=15)

        return view

    # =========================================================================
    # CORE LOGIC FOR PERSISTENCE / SAVING ACTIONS
    # =========================================================================
    def save_member_data(e):
        if selected_tier:
            filename = "primus_members.csv" if "Primus" in selected_tier else "aspirants_members.csv"
            path = os.path.join(ROOT, "data", filename)
            df = pd.read_csv(path, encoding='utf-8-sig')
            new_row = pd.DataFrame([{
                'STT': len(df) + 1, 'ingame': input_ingame.value,
                'tactical_role': input_role.value, 'status': input_status.value,
                'kda': input_kda.value, 'mvp_count': input_mvp.value
            }])
            pd.concat([df, new_row]).to_csv(path, index=False, encoding='utf-8-sig')
            close_dialog(None)
            if current_refresh_callback: current_refresh_callback()

    def save_tactic_data(e):
        if selected_tier:
            filename = "team_1.csv" if "Primus" in selected_tier else "team_2.csv"
            path = os.path.join(ROOT, "data", filename)
            df = pd.read_csv(path, encoding='utf-8-sig')
            new_row = pd.DataFrame([{
                'STT': len(df) + 1, 'title': input_tac_title.value,
                'category': input_tac_category.value, 'map_name': input_tac_map.value,
                'media_url': input_tac_url.value
            }])
            pd.concat([df, new_row]).to_csv(path, index=False, encoding='utf-8-sig')
            close_dialog(None)
            if current_refresh_callback: current_refresh_callback()

    def save_schedule_data(e):
        if selected_tier:
            filename = "primus_schedule.csv" if "Primus" in selected_tier else "aspirants_schedule.csv"
            path = os.path.join(ROOT, "data", filename)
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                df = pd.DataFrame(columns=['STT', 'type', 'title', 'opponent', 'date_time', 'result'])
            else:
                df = pd.read_csv(path, encoding='utf-8-sig')

            new_row = pd.DataFrame([{
                'STT': len(df) + 1, 'type': 'Event', 'title': input_sch_title.value,
                'opponent': input_sch_opponent.value, 'date_time': input_sch_datetime.value,
                'result': input_sch_result.value
            }])
            pd.concat([df, new_row]).to_csv(path, index=False, encoding='utf-8-sig')
            close_dialog(None)
            if current_refresh_callback: current_refresh_callback()

    # --- Setup Dialog Windows ---
    add_member_dialog = ft.AlertDialog(
        title=ft.Text("New Player / Member"),
        content=ft.Column([input_ingame, input_role, input_status, input_kda, input_mvp], width=300, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_member_data)],
        actions_alignment=ft.MainAxisAlignment.END
    )

    add_tactic_dialog = ft.AlertDialog(
        title=ft.Text("New Tactic / VOD Review"),
        content=ft.Column([input_tac_title, input_tac_category, input_tac_map, input_tac_url], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_tactic_data)],
        actions_alignment=ft.MainAxisAlignment.END
    )

    add_schedule_dialog = ft.AlertDialog(
        title=ft.Text("New Schedule / Scrim"),
        content=ft.Column([input_sch_title, input_sch_opponent, input_sch_datetime, input_sch_result], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_schedule_data)],
        actions_alignment=ft.MainAxisAlignment.END
    )

    # =========================================================================
    # SQUAD DASHBOARD CONTAINER RENDERING
    # =========================================================================
    def open_team_dashboard(tier_name):
        accent_color = ft.Colors.AMBER_400 if "Primus" in tier_name else ft.Colors.BLUE_400
        content_box = ft.Container(content=build_personnel_tab(tier_name), expand=True, padding=10)

        def tab_changed(e):
            idx = e.control.selected_index
            if idx == 0: content_box.content = build_personnel_tab(tier_name)
            elif idx == 1: content_box.content = build_tactics_tab(tier_name)
            elif idx == 2: content_box.content = build_schedule_tab(tier_name)
            elif idx == 3: content_box.content = build_statistics_tab(tier_name)
            content_box.update()

        def go_back_to_selector(e):
            nonlocal selected_tier
            selected_tier = None
            main_layout.content = tier_selector_view
            main_layout.update()

        # Bổ sung Tab 4: Analytics & Insights vào tab_bar
        tab_bar = ft.TabBar(tabs=[
            ft.Tab("Main Players", icon=ft.Icons.PEOPLE),
            ft.Tab("Tactics & VODs", icon=ft.Icons.LIGHTBULB_OUTLINED),
            ft.Tab("Schedule & Scrim", icon=ft.Icons.CALENDAR_MONTH),
            ft.Tab("Analytics & Insights", icon=ft.Icons.ANALYTICS_OUTLINED),
        ])

        inner_layout = ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.GREY_400, on_click=go_back_to_selector, tooltip="Back"),
                ft.Text(tier_name.upper(), size=22, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Container()
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            tab_bar, content_box
        ], expand=True)

        team_tabs = ft.Tabs(length=4, content=inner_layout, selected_index=0, on_change=tab_changed)
        main_layout.content = team_tabs
        main_layout.update()

    # =========================================================================
    # INITIAL TIER SELECTOR LANDING VIEW
    # =========================================================================
    def select_tier(tier_name, container_selected, container_other):
        nonlocal selected_tier
        selected_tier = tier_name
        container_selected.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE_54)
        container_other.border = ft.border.Border.all(1, ft.Colors.GREY_700)
        container_other.bgcolor = ft.Colors.BLACK
        if page: page.update()
        open_team_dashboard(selected_tier)

    primus_container = ft.Container(
        width=400, height=500, bgcolor="black", border=ft.border.Border.all(1, ft.Colors.GREY_700), border_radius=12, padding=15, alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Image(src="images/1st_IMT.png", width=400, height=350, fit="cover", border_radius=20),
                ft.Text("1st Killteam Primus", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                ft.Text("Killteam (Primus) Includes formal and S+ players gather to participate in tournaments", size=12, color=ft.Colors.GREY_300, text_align=ft.TextAlign.CENTER),
            ]
        )
    )

    aspirants_container = ft.Container(
        width=400, height=500, bgcolor="black", border=ft.border.Border.all(1, ft.Colors.GREY_700), border_radius=12, padding=15, alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Image(src="images/2st_IMTT.png", width=400, height=350, fit="cover", border_radius=20),
                ft.Text("2nd Aspirants Group", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                ft.Text("The Team of the Year (Tier 2). A training ground for promising players before join the first team.", size=12, color=ft.Colors.GREY_300, text_align=ft.TextAlign.CENTER),
            ]
        )
    )

    primus_container.on_click = lambda e: select_tier("1st Killteam Primus", primus_container, aspirants_container)
    aspirants_container.on_click = lambda e: select_tier("2nd Aspirants Group", aspirants_container, primus_container)

    tier_selector_view = ft.Column(
        controls=[
            ft.Row([ft.Text("Select Team Tier", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Select your team tier to start !!!", color=ft.Colors.GREY_400),
            ft.Row(controls=[primus_container, aspirants_container], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
    )

    main_layout.content = tier_selector_view
    return main_layout

def settings_view(page: ft.Page):
    '''Returns an English localized modular configuration setting view panel'''
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_button.icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.DARK_MODE
        theme_button.text = "Switch to Dark Mode" if page.theme_mode == ft.ThemeMode.LIGHT else "Switch to Light Mode"
        page.update()

    theme_button = ft.ElevatedButton(
        "Switch to Light Mode" if page.theme_mode == ft.ThemeMode.DARK else "Switch to Dark Mode",
        icon=ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE,
        on_click=toggle_theme
    )

    return ft.Container(
        padding=30,
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.SETTINGS, size=28, color=ft.Colors.BLUE_ACCENT), ft.Text("APPLICATION SETTINGS", size=24, weight=ft.FontWeight.BOLD)]),
            ft.Divider(),
            ft.Text("Appearance", size=18, weight=ft.FontWeight.W_600),
            theme_button,
            ft.Container(height=15),
            ft.Text("System Parameters", size=18, weight=ft.FontWeight.W_600),
            ft.Text("Language: English (Default)", size=14, color=ft.Colors.GREY_400),
            ft.Text("Data sync engine: Enabled (CSV Auto-save)", size=14, color=ft.Colors.GREY_400),
            ft.Divider(),
            ft.Text("Illuminati Management App v2.1.0", size=12, color=ft.Colors.GREY_600)
        ])
    )

def main(page: ft.Page):
    page.title = "Illuminati Team Management"
    page.theme_mode = ft.ThemeMode.DARK
    
    def save_time(e: ft.ControlEvent):
        if match_time.value:
            time_result.value = f"{match_time.value.hour:02d}:{match_time.value.minute:02d}"
        else:
            time_result.value = "00:00"
        time_result.update()
        
    clan_input = ft.TextField(label="Clan", width=300)
    ingame_input = ft.TextField(label="Nickname (Ingame)", width=300)
    media_input = ft.TextField(label="Media (Facebook URL)", width=300)
    role_input = ft.TextField(label="Role", width=300)
    note_input = ft.TextField(label="Note", width=300, multiline=True)
    
    date = ft.TextField(label="Date", width=100)
    month = ft.TextField(label="Month", width=100)
    year = ft.TextField(label="Year", width=100)
    clan_opponent = ft.TextField(label="Opponent Clan", width=300)
    mode_selection = ft.Dropdown(
        options=[
            ft.DropdownOption(key="Hard point", text="HP"),
            ft.DropdownOption(key="Search & Destroy", text="C4"),
            ft.DropdownOption(key="Domination", text="ABC"),
            ft.DropdownOption(key="Control", text="CT"),
            ft.DropdownOption(key="Team Deathmatch", text="TDM"),
            ft.DropdownOption(key="Frontline", text="FL"),
            ft.DropdownOption(key="Hardpoint & SD", text="HP - C4"),
            ft.DropdownOption(key="Hardpoint, Controls & SD", text="HP - CTs - C4"),
        ],
        width=300, label="Mode"
    )
    note = ft.TextField(label="Note", multiline=True, max_lines=10)
    time_result = ft.TextField(value="00:00", width=200)
    
    match_time = ft.TimePicker(open=True, value=time(1, 2), entry_mode=ft.TimePickerEntryMode.INPUT_ONLY, on_change=save_time)
    pick_time_button = ft.ElevatedButton("Select Time", on_click=lambda e: page.show_dialog(match_time), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(), color="white", bgcolor="blue"))
    
    date_event = ft.TextField(label="Day", width=90)
    month_event = ft.TextField(label="Month", width=90)
    year_event = ft.TextField(label="Year", width=100)
    event_name = ft.TextField(label="Event Title")
    event_content = ft.TextField(label="Content Summary", multiline=True, min_lines=3)
    
    date_note = ft.TextField(label="Day", width=90)
    month_note = ft.TextField(label="Month", width=90)
    year_note = ft.TextField(label="Year", width=100)
    note_title_input = ft.TextField(label="Note Title")
    note_content_input = ft.TextField(label="Detailed Notes", multiline=True, min_lines=3)

    def close_dialog(e):
        add_dialog.open = False
        match_dialog.open = False

    def save_match(e):
        if os.path.exists(MATCH_PATH):
            try: df = pd.read_csv(MATCH_PATH, encoding='utf-8-sig'); next_stt = len(df) + 1
            except: df = pd.DataFrame(); next_stt = 1
        else: df = pd.DataFrame(); next_stt = 1
        full_date = f"{date.value}/{month.value}/{year.value}"
        new_data = {'STT': [next_stt], 'Date': [full_date], 'Time': [time_result.value], 'Clan': [clan_opponent.value], 'Mode': [mode_selection.value], 'Note': [note.value]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        os.makedirs(os.path.dirname(MATCH_PATH), exist_ok=True)
        df.to_csv(MATCH_PATH, index=False, encoding='utf-8-sig')
        date.value = ""; month.value = ""; year.value = ""; time_result.value = "00:00"; clan_opponent.value = ""; mode_selection.value = None; note.value = ""
        match_dialog.open = False
        if hasattr(match_view, 'custom_refresh'): match_view.custom_refresh()

    def save_member(e):
        if os.path.exists(MEMBERS_PATH):
            try: df = pd.read_csv(MEMBERS_PATH, encoding='utf-8-sig'); next_stt = len(df) + 1
            except: df = pd.DataFrame(); next_stt = 1
        else: df = pd.DataFrame(); next_stt = 1
        new_data = {'STT': [next_stt], 'Clan': [clan_input.value], 'ingame': [ingame_input.value], 'media': [media_input.value], 'role': [role_input.value], 'note': [note_input.value]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        os.makedirs(os.path.dirname(MEMBERS_PATH), exist_ok=True)
        df.to_csv(MEMBERS_PATH, index=False, encoding='utf-8-sig')
        clan_input.value = ""; ingame_input.value = ""; media_input.value = ""; role_input.value = ""; note_input.value = ""
        add_dialog.open = False
        if hasattr(table_view, 'custom_refresh'): table_view.custom_refresh()

    def save_event(e):
        if os.path.exists(EVENT_PATH):
            try: df = pd.read_csv(EVENT_PATH, encoding='utf-8-sig'); next_stt = len(df) + 1
            except: df = pd.DataFrame(); next_stt = 1
        else: df = pd.DataFrame(); next_stt = 1
        full_date = f"{date_event.value}/{month_event.value}/{year_event.value}"
        new_data = {'STT': [next_stt], 'name': [event_name.value], 'content': [event_content.value], 'date': [full_date]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        os.makedirs(os.path.dirname(EVENT_PATH), exist_ok=True)
        df.to_csv(EVENT_PATH, index=False, encoding='utf-8-sig')
        date_event.value = ""; month_event.value = ""; year_event.value = ""; event_name.value = ""; event_content.value = ""
        events_dialog.open = False
        if hasattr(event_view, 'custom_refresh'): event_view.custom_refresh()

    def save_note(e):
        if os.path.exists(NOTE_PATH):
            try: df = pd.read_csv(NOTE_PATH, encoding='utf-8-sig'); next_stt = len(df) + 1
            except: df = pd.DataFrame(); next_stt = 1
        else: df = pd.DataFrame(); next_stt = 1
        full_date = f"{date_note.value}/{month_note.value}/{year_note.value}"
        new_data = {'STT': [next_stt], 'name': [note_title_input.value], 'content': [note_content_input.value], 'date': [full_date]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        os.makedirs(os.path.dirname(NOTE_PATH), exist_ok=True)
        df.to_csv(NOTE_PATH, index=False, encoding='utf-8-sig')
        date_note.value = ""; month_note.value = ""; year_note.value = ""; note_title_input.value = ""; note_content_input.value = ""
        notes_dialog.open = False
        if hasattr(notes_view, 'custom_refresh'): notes_view.custom_refresh()

    add_options_dialog = ft.AlertDialog(
        title=ft.Text("Options Menu"),
        actions=[
            ft.TextButton("New Member", on_click=lambda e: [page.close_dialog(), page.show_dialog(add_dialog)]),
            ft.TextButton("New Custom Match", on_click=lambda e: [page.close_dialog(), page.show_dialog(match_dialog)]),
            ft.TextButton("New Event", on_click=lambda e: [page.close_dialog(), page.show_dialog(events_dialog)]),
            ft.TextButton("New Note", on_click=lambda e: [page.close_dialog(), page.show_dialog(notes_dialog)]),
        ],
    )
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("Add New Member Record"),
        content=ft.Column(controls=[clan_input, ingame_input, media_input, role_input, note_input], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_member)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    match_dialog = ft.AlertDialog(
        title=ft.Text("Log Custom Match Record"),
        content=ft.Column(controls=[ft.Row([date, month, year]), ft.Row([pick_time_button, time_result]), clan_opponent, mode_selection, note], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_match)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    events_dialog = ft.AlertDialog(
        title=ft.Text("Create New Event Scheduling"),
        content=ft.Column(controls=[ft.Row([date_event, month_event, year_event]), event_name, event_content], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_event)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    notes_dialog = ft.AlertDialog(
        title=ft.Text("Add New Canvas Annotation Note"),
        content=ft.Column(controls=[ft.Row([date_note, month_note, year_note]), note_title_input, note_content_input], tight=True, spacing=10),
        actions=[ft.TextButton("Cancel", on_click=close_dialog), ft.ElevatedButton("Save", bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=save_note)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    table_view = members_table(page)
    match_view = match_table(page)
    event_view = event_table(page)
    notes_view = event_cards_view(page)  
    academy_view = academy_tier_selector(page)
    summarize_view = summary_view(page)
    config_setting_view = settings_view(page)

    content_container = ft.Container(content=summarize_view, expand=True, padding=20)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            content_container.content = summarize_view
            if hasattr(summarize_view, 'custom_refresh'): summarize_view.custom_refresh()
        elif idx == 1:
            content_container.content = table_view
            if hasattr(table_view, 'custom_refresh'): table_view.custom_refresh()
        elif idx == 2:
            content_container.content = match_view
            if hasattr(match_view, 'custom_refresh'): match_view.custom_refresh()
        elif idx == 3:
            content_container.content = event_view
            if hasattr(event_view, 'custom_refresh'): event_view.custom_refresh()
        elif idx == 4:
            content_container.content = notes_view
            if hasattr(notes_view, 'custom_refresh'): notes_view.custom_refresh()
        elif idx == 5:
            content_container.content = academy_view
        elif idx == 6:
            content_container.content = config_setting_view
            
        content_container.update()

    rail = ft.NavigationRail(
        margin=-10, selected_index=0, label_type=ft.NavigationRailLabelType.ALL, min_width=100, min_extended_width=400, group_alignment=-0.9, on_change=on_nav_change,
        bgcolor="black", indicator_color="black",
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, content="Add", on_click=lambda e: page.show_dialog(add_options_dialog), bgcolor="black"),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, selected_icon=ft.Icons.BAR_CHART, label="Summary"),
            ft.NavigationRailDestination(icon=ft.Icons.LIST, selected_icon=ft.Icons.LIST, label="Members"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.GAMEPAD), selected_icon=ft.Icon(ft.Icons.GAMEPAD), label="Match Custom"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.EVENT), selected_icon=ft.Icon(ft.Icons.EVENT), label="Events"),
            ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.NOTE), selected_icon=ft.Icon(ft.Icons.NOTE), label="Notes"),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK_ONLINE, selected_icon=ft.Icons.BOOK_ONLINE, label="Academy"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
        ],
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.SelectionArea(content=rail),
                    ft.VerticalDivider(width=1),
                    ft.Column(alignment=ft.MainAxisAlignment.START, expand=True, controls=[content_container]),
                ],
            ),
        )
    )
    
    page.fonts = {"COD": 'fonts/JetBrainsMono-VariableFont_wght.ttf'}
    page.theme = ft.Theme(font_family="COD")
    page.foreground_decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b253b0f9-a780-492d-9e1a-f3eb38eb4cdf/dgnqagb-9317addb-ab22-47d3-aa27-e48890071bda.jpg/v1/fill/w_1237,h_646,q_70,strp/konni_group_by_thatguyintheshadows_dgnqagb-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjY5IiwicGF0aCI6Ii9mL2IyNTNiMGY5LWE3ODAtNDkyZC05ZTFhLWYzZWIzOGViNGNkZi9kZ25xYWdiLTkzMTdhZGRiLWFiMjItNDdkMy1hYTI3LWU0ODg5MDA3MWJkYS5qcGciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.7DgmVPVQjDkibCTPfXTHEEMpNhr2HKhGnzQapaXVGKo",
            fit="Cover", opacity=0.10
        )
    )

if __name__ == "__main__":
    ft.run(main, assets_dir='assets')