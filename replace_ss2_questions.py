import re

html_file = 'ECONS & GEO ss2.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_bank = '''        const bank = [
            {
                subject: "ECONOMICS",
                questions: [
                    {
                        q: "Which of the following best describes 'Economic Development Planning' in a developing nation like Nigeria?",
                        options: ["The random allocation of resources without government intervention", "A deliberate government effort to coordinate resources to achieve specific socio-economic goals over a period", "The reliance entirely on foreign aid to build local industries", "The exclusive focus on military expansion and defense budgets"],
                        ans: 1
                    },
                    {
                        q: "What is a major problem hindering successful economic planning in Nigeria?",
                        options: ["Overabundance of accurate statistical data", "Excessive technological advancement", "Corruption and inadequate reliable data", "Perfect political stability"],
                        ans: 2
                    },
                    {
                        q: "Which type of economic plan is designed to cover a very short duration, usually one financial year?",
                        options: ["Perspective Plan", "Rolling Plan", "Annual Plan", "Decade Plan"],
                        ans: 2
                    },
                    {
                        q: "The primary objective of the International Monetary Fund (IMF) is to:",
                        options: ["Provide long-term loans for infrastructure like dams and roads", "Promote global exchange rate stability and assist with balance of payment difficulties", "Regulate the global price of crude oil", "Distribute free food during humanitarian crises"],
                        ans: 1
                    },
                    {
                        q: "Which international economic organization was established primarily to provide long-term capital assistance for post-war reconstruction and development?",
                        options: ["World Trade Organization (WTO)", "Economic Community of West African States (ECOWAS)", "International Bank for Reconstruction and Development (World Bank)", "African Union (AU)"],
                        ans: 2
                    },
                    {
                        q: "Which of the following is NOT an objective of ECOWAS?",
                        options: ["Promoting intra-regional trade", "Fostering economic integration in West Africa", "Establishing a common currency among member states", "Imposing tariffs on trade between member states"],
                        ans: 3
                    },
                    {
                        q: "The World Trade Organization (WTO) succeeded which international agreement?",
                        options: ["The Bretton Woods Agreement", "The General Agreement on Tariffs and Trade (GATT)", "The North American Free Trade Agreement (NAFTA)", "The Paris Club"],
                        ans: 1
                    },
                    {
                        q: "What was the core target of the Millennium Development Goals (MDGs) before its expiration in 2015?",
                        options: ["To eradicate extreme poverty and hunger globally", "To colonize developing nations", "To increase global carbon emissions", "To eliminate all national borders in Africa"],
                        ans: 0
                    },
                    {
                        q: "NEEDS (National Economic Empowerment and Development Strategy) was an initiative launched in Nigeria to:",
                        options: ["Increase the importation of finished goods", "Promote wealth creation, employment generation, and poverty reduction", "Ensure government monopoly in all business sectors", "Ban all foreign direct investment"],
                        ans: 1
                    },
                    {
                        q: "The 'Vision 20:2020' economic plan in Nigeria aimed to:",
                        options: ["Make Nigeria one of the top 20 economies in the world by the year 2020", "Reduce the population of Nigeria to 20 million", "Ensure 20% of Nigerians migrate abroad", "Increase inflation by 20% annually"],
                        ans: 0
                    },
                    {
                        q: "Which of the following is a significant challenge to economic development in West Africa?",
                        options: ["High rates of technological innovation", "Low population growth rates", "Poor infrastructure and erratic power supply", "Excessive agricultural surpluses"],
                        ans: 2
                    },
                    {
                        q: "How does corruption affect the economic development of a country?",
                        options: ["It accelerates infrastructural growth", "It diverts public funds into private pockets, stifling development", "It encourages foreign direct investment", "It improves the standard of living for all citizens"],
                        ans: 1
                    },
                    {
                        q: "The Structural Adjustment Programme (SAP) was introduced in Nigeria in 1986 primarily to:",
                        options: ["Increase government spending on subsidies", "Restructure and diversify the productive base of the economy", "Peg the Naira to the Dollar permanently", "Nationalize all foreign banks"],
                        ans: 1
                    },
                    {
                        q: "Which policy involves the transfer of ownership and control of public enterprises to private individuals?",
                        options: ["Commercialization", "Nationalization", "Indigenization", "Privatization"],
                        ans: 3
                    },
                    {
                        q: "Deregulation of an economy implies:",
                        options: ["The removal of government controls and restrictions to allow free market forces", "The government taking full control of all pricing", "The banning of imported goods", "The introduction of strict price ceilings on all products"],
                        ans: 0
                    },
                    {
                        q: "What is the main difference between privatization and commercialization?",
                        options: ["Privatization involves change of ownership, while commercialization makes public enterprises profit-oriented without changing ownership", "Commercialization involves selling shares, while privatization involves giving them away", "They are exactly the same concept", "Privatization only applies to agriculture"],
                        ans: 0
                    },
                    {
                        q: "Which of these is a benefit of economic reform programs like deregulation?",
                        options: ["Creation of state monopolies", "Increased competition leading to better service delivery and efficiency", "Complete eradication of taxes", "Increased government bureaucracy"],
                        ans: 1
                    },
                    {
                        q: "What is the primary role of the African Union (AU) in the economic context?",
                        options: ["To issue a single currency for the entire world", "To promote socio-economic integration and sustainable development in Africa", "To monitor global oil prices", "To provide military aid to European countries"],
                        ans: 1
                    },
                    {
                        q: "A high dependency ratio in a country's population structure poses what economic challenge?",
                        options: ["It leads to excessive savings and capital formation", "It puts a strain on the working population and national resources", "It automatically increases agricultural output", "It completely eliminates unemployment"],
                        ans: 1
                    },
                    {
                        q: "Which of the following best defines 'Poverty' in an economic development context?",
                        options: ["The inability to afford luxury vehicles", "A state where an individual lacks the financial resources to meet basic needs like food, shelter, and clothing", "Earning less than a millionaire", "Living in a rural area"],
                        ans: 1
                    }
                ]
            },
            {
                subject: "GEOGRAPHY",
                questions: [
                    {
                        q: "In map reading, the angular distance measured clockwise from the North to a given point is known as:",
                        options: ["Latitude", "Longitude", "Bearing", "Scale"],
                        ans: 2
                    },
                    {
                        q: "If the forward bearing of Town A from Town B is 045°, what is the back bearing of Town B from Town A?",
                        options: ["225°", "135°", "315°", "045°"],
                        ans: 0
                    },
                    {
                        q: "Which of the following is the most accurate method of showing relief on a topographical map?",
                        options: ["Hachures", "Spot heights", "Contour lines", "Layer colouring"],
                        ans: 2
                    },
                    {
                        q: "Lines drawn on a map joining places of equal elevation above sea level are called:",
                        options: ["Isobars", "Isohyets", "Contours", "Isotherms"],
                        ans: 2
                    },
                    {
                        q: "When contour lines are very far apart on a map, they indicate:",
                        options: ["A steep slope", "A gentle slope", "A vertical cliff", "A deep valley"],
                        ans: 1
                    },
                    {
                        q: "Which of the following factors strongly influences the distribution of human population?",
                        options: ["Longitude", "Relief and climate", "Time zones", "Ocean currents"],
                        ans: 1
                    },
                    {
                        q: "A population structure with a very broad base and a narrow top indicates:",
                        options: ["An aging population", "A high birth rate and a youthful population", "A low death rate", "A declining population"],
                        ans: 1
                    },
                    {
                        q: "Overpopulation occurs when:",
                        options: ["There are too many people in a country regardless of resources", "The available resources cannot adequately support the existing population", "The birth rate equals the death rate", "People migrate to urban areas"],
                        ans: 1
                    },
                    {
                        q: "Which of the following is a characteristic feature of a rural settlement?",
                        options: ["High population density", "Primary occupations like farming and fishing", "Complex road networks and skyscrapers", "Availability of large industrial estates"],
                        ans: 1
                    },
                    {
                        q: "A settlement pattern where buildings are grouped closely together around a central feature like a crossroad or market is called:",
                        options: ["Dispersed settlement", "Linear settlement", "Nucleated settlement", "Isolated settlement"],
                        ans: 2
                    },
                    {
                        q: "What is a major cause of rural-urban migration in developing countries?",
                        options: ["The desire to engage in agriculture", "Search for better employment opportunities and social amenities", "The need to enjoy a quiet and peaceful environment", "Abundance of cheap land in the cities"],
                        ans: 1
                    },
                    {
                        q: "Which of the following is an effect of rural-urban migration on the rural areas?",
                        options: ["Overcrowding and traffic congestion", "Decline in agricultural workforce and production", "Increase in industrialization", "Improved standard of living"],
                        ans: 1
                    },
                    {
                        q: "A major geo-political issue that frequently causes conflict between neighboring African countries is:",
                        options: ["Boundary and territorial disputes", "Similarity in cultural festivals", "Shared language dialects", "Common currency usage"],
                        ans: 0
                    },
                    {
                        q: "In Geographic Information Systems (GIS), data that describes the characteristics or qualities of a spatial feature is known as:",
                        options: ["Spatial data", "Attribute data", "Vector data", "Raster data"],
                        ans: 1
                    },
                    {
                        q: "Which of the following is a primary source of data for GIS?",
                        options: ["Newspaper articles", "Oral traditions", "Satellite imagery and aerial photography", "Fictional novels"],
                        ans: 2
                    },
                    {
                        q: "The sudden shaking of the earth's crust caused by the release of energy in the lithosphere is called:",
                        options: ["Vulcanicity", "An Earthquake", "Folding", "Weathering"],
                        ans: 1
                    },
                    {
                        q: "Which landform is primarily created by the process of faulting?",
                        options: ["Fold mountain", "Rift valley", "Volcanic cone", "Delta"],
                        ans: 1
                    },
                    {
                        q: "The process by which molten magma from the earth's interior is forced into the crust or onto the surface is known as:",
                        options: ["Folding", "Faulting", "Vulcanicity", "Denudation"],
                        ans: 2
                    },
                    {
                        q: "Which of the following is a feature formed by folding?",
                        options: ["Block mountain", "Anticlines and Synclines", "Horst", "Crater"],
                        ans: 1
                    },
                    {
                        q: "What term describes the point on the earth's surface directly above the origin of an earthquake?",
                        options: ["Hypocenter", "Focus", "Epicenter", "Seismic wave"],
                        ans: 2
                    }
                ]
            }
        ];'''

# Replace the existing bank
# The bank starts at "        const bank = [" and ends at "        ];" (before "let activeSubjectIdx = 0;")
pattern = re.compile(r'        const bank = \[.*?        \];', re.DOTALL)
new_content = pattern.sub(new_bank, content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SS2 Questions Successfully Generated and Injected!")
