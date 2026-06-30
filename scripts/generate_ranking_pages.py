import os

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RANKINGS_DIR = os.path.join(PROJECT_ROOT, "frames", "rankings")

def generate_html_template(division_name, division_id):
    """Generate HTML content for a division ranking page."""
    return f'''<!doctype html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{division_name} Rankings - Bebops Zottegem</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Open+Sans:wght@400;600;700&display=swap"
      rel="stylesheet"
    />
    <style>
      :root {{
        --primary-color: #c41e3a;
        --secondary-color: #ffffff;
        --accent-color: #1a1a1a;
        --text-light: #ffffff;
        --text-dark: #333;
      }}

      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}

      html,
      body {{
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Open Sans", sans-serif;
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
      }}

      .header-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100px;
        background: linear-gradient(
          135deg,
          var(--primary-color) 0%,
          #8b0000 100%
        );
        display: flex;
        align-items: center;
        padding: 0 50px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 1000;
      }}

      .header-overlay::after {{
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--secondary-color);
      }}

      .logo-container {{
        display: flex;
        align-items: center;
        gap: 25px;
      }}

      .club-logo {{
        height: 70px;
        width: auto;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
      }}

      .club-text {{
        display: flex;
        flex-direction: column;
      }}

      .club-name {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 3rem;
        color: var(--text-light);
        letter-spacing: 3px;
        line-height: 1;
      }}

      .club-subtitle {{
        font-family: "Open Sans", sans-serif;
        font-size: 1.1rem;
        color: var(--secondary-color);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 5px;
        opacity: 0.9;
      }}

      .content {{
        position: absolute;
        top: 100px;
        left: 0;
        right: 0;
        bottom: 0;
        padding: 15px 40px;
        display: flex;
        flex-direction: column;
      }}

      .rankings-container {{
        flex: 1;
        display: flex;
        flex-direction: column;
        max-width: 1400px;
        width: 100%;
        margin: 0 auto;
      }}

      .division-section {{
        flex: 1;
        display: flex;
        flex-direction: column;
      }}

      .division-title {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 2rem;
        color: var(--primary-color);
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 10px;
        text-align: center;
      }}

      .table-wrapper {{
        display: inline-block;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        width: 100%;
      }}

      .rankings-table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
      }}

      .rankings-table thead {{
        background: linear-gradient(
          135deg,
          var(--primary-color) 0%,
          #8b0000 100%
        );
        color: var(--text-light);
      }}

      .rankings-table th {{
        padding: 12px 10px;
        font-family: "Bebas Neue", sans-serif;
        font-size: 1.2rem;
        letter-spacing: 2px;
        text-align: left;
      }}

      .rankings-table th.center,
      .rankings-table td.center {{
        text-align: center;
      }}

      .rankings-table tbody tr {{
        border-bottom: 1px solid #f0f0f0;
      }}

      .rankings-table tbody tr.bebops {{
        background-color: #fff5f5;
        font-weight: 600;
      }}

      .rankings-table td {{
        padding: 10px;
        font-size: 1rem;
        color: var(--text-dark);
      }}

      .team-cell {{
        display: flex;
        align-items: center;
        gap: 12px;
      }}

      .team-logo {{
        width: 32px;
        height: 32px;
        object-fit: contain;
        flex-shrink: 0;
      }}

      .team-name {{
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}

      .rank-cell {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 1.3rem;
        color: var(--primary-color);
        font-weight: bold;
      }}

      .stats-cell {{
        font-weight: 600;
      }}

      /* Column widths */
      .rankings-table th:nth-child(1),
      .rankings-table td:nth-child(1) {{ width: 50px; }}
      .rankings-table th:nth-child(3),
      .rankings-table td:nth-child(3),
      .rankings-table th:nth-child(4),
      .rankings-table td:nth-child(4),
      .rankings-table th:nth-child(5),
      .rankings-table td:nth-child(5) {{ width: 50px; }}
      .rankings-table th:nth-child(6),
      .rankings-table td:nth-child(6),
      .rankings-table th:nth-child(7),
      .rankings-table td:nth-child(7) {{ width: 70px; }}
    </style>
  </head>
  <body>
    <div class="header-overlay">
      <div class="logo-container">
        <img
          src="https://bjarnevanwijmeersch1-bebops.github.io/bebops-data/images/logo.png"
          alt="Bebops"
          class="club-logo"
        />
        <div class="club-text">
          <span class="club-name">Bebops</span>
          <span class="club-subtitle">Baseball- & Softballclub</span>
        </div>
      </div>
    </div>

    <div class="content">
      <div class="rankings-container">
        <div id="{division_id}-section" class="division-section">
          <div class="division-title">{division_name}</div>
          <div class="table-wrapper">
            <table class="rankings-table">
              <thead>
                <tr>
                  <th class="center">#</th>
                  <th>Team</th>
                  <th class="center">W</th>
                  <th class="center">L</th>
                  <th class="center">T</th>
                  <th class="center">PCT</th>
                  <th class="center">GB</th>
                </tr>
              </thead>
              <tbody id="{division_id}-tbody">
                <tr>
                  <td colspan="7" class="center">Loading...</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <script>
      // Auto-detect if running locally or on GitHub Pages
      const isLocal = window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const DATA_BASE_URL = isLocal
        ? '../../data/rankings/'
        : 'https://bjarnevanwijmeersch1-bebops.github.io/bebops-data/data/rankings/';

      function isBebopsTeam(teamName) {{
        return teamName && teamName.toLowerCase().includes('bebops');
      }}

      function createTeamRow(team) {{
        const row = document.createElement('tr');
        if (isBebopsTeam(team['Team.1'])) {{
          row.classList.add('bebops');
        }}

        row.innerHTML = `
          <td class="center rank-cell">${{team['#']}}</td>
          <td>
            <div class="team-cell">
              ${{team['Team'] ? `<img src="${{team['Team']}}" alt="Team Logo" class="team-logo" />` : ''}}
              <span class="team-name">${{team['Team.1']}}</span>
            </div>
          </td>
          <td class="center stats-cell">${{team['W']}}</td>
          <td class="center stats-cell">${{team['L']}}</td>
          <td class="center stats-cell">${{team['T']}}</td>
          <td class="center">${{team['PCT'].toFixed(3)}}</td>
          <td class="center">${{team['GB'] === 0 ? '-' : team['GB'].toFixed(1)}}</td>
        `;

        return row;
      }}

      function scaleTableToFit() {{
        const content = document.querySelector('.content');
        const tableWrapper = document.querySelector('.table-wrapper');
        const table = document.querySelector('.rankings-table');
        const title = document.querySelector('.division-title');

        // Reset any previous scaling
        tableWrapper.style.transform = '';
        tableWrapper.style.transformOrigin = 'top center';

        // Calculate available height (content area minus title and padding)
        const contentHeight = content.clientHeight;
        const titleHeight = title.offsetHeight + 10;
        const availableHeight = contentHeight - titleHeight;

        // Get table actual height
        const tableHeight = table.offsetHeight;

        // If table is taller than available space, scale it down
        if (tableHeight > availableHeight) {{
          const scale = availableHeight / tableHeight;
          tableWrapper.style.transform = `scale(${{scale}})`;
          tableWrapper.style.height = `${{tableHeight}}px`;
        }}
      }}

      async function loadRankings() {{
        try {{
          const {division_id}Response = await fetch(`${{DATA_BASE_URL}}{division_id.upper()}.json`);
          const {division_id}Data = await {division_id}Response.json();
          const {division_id}Tbody = document.getElementById('{division_id}-tbody');
          {division_id}Tbody.innerHTML = '';
          {division_id}Data.forEach(team => {{
            {division_id}Tbody.appendChild(createTeamRow(team));
          }});

          // Scale table to fit viewport after loading
          setTimeout(scaleTableToFit, 100);
        }} catch (error) {{
          console.error('Error loading rankings:', error);
          document.getElementById('{division_id}-tbody').innerHTML = '<tr><td colspan="7" class="center">Error loading rankings</td></tr>';
        }}
      }}

      // Rescale on window resize
      window.addEventListener('resize', scaleTableToFit);

      loadRankings();
    </script>
  </body>
</html>
'''

def generate_ranking_pages():
    """Generate ranking HTML pages for all divisions."""
    divisions = [
        ("Division 2", "d2"),
        ("Division 3", "d3"),
        ("U15", "u15"),
        ("U12", "u12"),
        ("Softball Ladies D3", "sd3")
    ]

    # Ensure rankings directory exists
    os.makedirs(RANKINGS_DIR, exist_ok=True)

    for division_name, division_id in divisions:
        html_content = generate_html_template(division_name, division_id)
        filename = os.path.join(RANKINGS_DIR, f"{division_id.upper()}.html")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[OK] Generated {filename}")

if __name__ == "__main__":
    generate_ranking_pages()
    print("All ranking pages generated successfully!")
